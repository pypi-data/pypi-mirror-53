import logging
import os
from configparser import ConfigParser
from hashlib import sha256
from yaml import safe_load

from pandoc_compose.utils import PANDOC_COMPOSE_HASH_FILE_NAME, HASH_DEFAULT_SECTION, logger
from pandoc_compose.errors import PandocConfigNotFoundError
from pandoc_compose.pandoc_config import PandocConfig


class PandocComposeConfig:
    def __init__(self, cli_args, *args):
        self.destination = os.path.join(cli_args.dest, "")
        self.pandoc_config = None
        self.timeout = 0
        self.force = False
        self.hash_file_path = None
        self.hash_config = {}
        self.pandoc_config_file_hash = None

        config_file_path = PandocConfig.get_config_file_path(self.destination)
        if not os.path.exists(config_file_path):
            raise PandocConfigNotFoundError(config_file_path)

        # pandoc-compose must be configure before pandoc_config is initialized since it sets the logger level
        original_config = self.__read_config(config_file_path)
        pandoc_compose_config = original_config.pop("pandoc_compose_options", {})
        self.__init_pandoc_compose_config(pandoc_compose_config, cli_args)

        self.pandoc_config = PandocConfig(config_file_path, original_config)

        if len(list(args)) > 0:
            self.pandoc_config = self.pandoc_config.merge({"pandoc_options": args})

        self.__init_hash_config()

    def __init_hash_config(self):
        self.pandoc_config_file_hash = self.get_file_hash(self.pandoc_config.config_file_path)

        self.hash_file_path = os.path.join(self.destination, PANDOC_COMPOSE_HASH_FILE_NAME)

        if os.path.exists(self.hash_file_path):
            cp = ConfigParser()
            # https://stackoverflow.com/questions/19359556/configparser-reads-capital-keys-and-make-them-lower-case
            cp.optionxform = str
            cp.read(self.hash_file_path)
            try:
                self.hash_config = dict(cp[HASH_DEFAULT_SECTION])
            except KeyError:
                self.hash_config = {}

    def __init_pandoc_compose_config(self, pandoc_compose_original_config, cli_args):
        level = logging.getLevelName({1: "WARNING", 2: "INFO", 3: "DEBUG"}.get(cli_args.verbose))
        if isinstance(level, int):
            logger.setLevel(level)
        else:
            verbose = pandoc_compose_original_config.get("verbose")
            level = logging.getLevelName(verbose)
            if isinstance(level, int):
                logger.setLevel(level)

        timeout = (
            cli_args.timeout if cli_args.timeout is not None else pandoc_compose_original_config.get("timeout", "10m")
        )
        self.timeout = self.__compute_timeout(timeout)

        self.force = cli_args.force or pandoc_compose_original_config.get("force", False)

    @staticmethod
    def get_file_hash(fname):
        def file_as_blockiter(blocksize=65536):
            with open(fname, "rb") as f:
                block = f.read(blocksize)
                while len(block) > 0:
                    yield block
                    block = f.read(blocksize)

        file_hash = sha256()

        for chunk in file_as_blockiter():
            file_hash.update(chunk)

        return file_hash.hexdigest()

    @staticmethod
    def __compute_timeout(timeout):
        try:
            if timeout.endswith("h"):
                return int(timeout[:-1]) * 60 * 60
            elif timeout.endswith("m"):
                return int(timeout[:-1]) * 60
            elif timeout.endswith("s"):
                return int(timeout[:-1])
            else:
                return int(timeout)
        except ValueError:
            raise PandocComposeGenericError("--timeout option is not correct")

    @staticmethod
    def __read_config(config_file_path):
        with open(config_file_path, mode="r") as f:
            _config = safe_load(f)
            return _config if isinstance(_config, dict) else {}
