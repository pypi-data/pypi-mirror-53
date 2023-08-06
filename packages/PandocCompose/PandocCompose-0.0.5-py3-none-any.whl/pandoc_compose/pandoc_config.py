import os
from json import dumps as json_dumps
from deepmerge import always_merger

from pandoc_compose.utils import KNOWN_TARGET_FORMATS, KNOWN_SOURCE_FORMATS, PANDOC_COMPOSE_FILE, logger
from pandoc_compose.errors import PandocComposeGenericError, TaskGlobYouDidEveryWrongError
from pandoc_compose.convert_task_glob_handler import normalise


class PandocConfig:
    def __init__(self, config_file_path, original_config, merging=False):
        self.config_file_path = config_file_path
        self.__original_config = original_config.copy()
        # When merging two config, we expect files have already been processed
        # so files section in original config should be correct
        if not merging:
            self.__process_files_section()

    @property
    def files(self):
        return self.__original_config.get("files")

    @files.setter
    def files(self, value):
        self.__original_config["files"] = value

    @property
    def pandoc(self):
        return self.__original_config.get("pandoc", {})

    @property
    def pandoc_options(self):
        return self.__original_config.get("pandoc_options", {})

    def merge(self, config_override):
        new_config = always_merger.merge(self.__original_config.copy(), config_override)
        return PandocConfig(self.config_file_path, new_config, merging=True)

    def __process_files_section(self):
        fallback_msg = 'Falling back to default [{"**/*.md": {"from": "markdown", "to": "pdf"}}]'
        files = self.files
        if not isinstance(files, list) or len(files) == 0:
            logger.debug("`files` section is empty, %s", fallback_msg)
            self.files = self.__default_files_list()
            return

        new_files = []
        for idx, file in enumerate(files):
            try:
                new_files.append(normalise(file, idx))
            except TaskGlobYouDidEveryWrongError as e:
                logger.error(e)
            except PandocComposeGenericError as e:
                logger.warning(e)
        if len(new_files) == 0:
            logger.warning("No valid item found `files` section of %s; %s", self.config_file_path, fallback_msg)
            self.files = self.__default_files_list()
        else:
            self.files = new_files

    @staticmethod
    def __default_files_list():
        return [{"**/*.md": {"from": "markdown", "to": ["pdf"]}}]

    def __str__(self):
        return json_dumps(self.__original_config, indent=4, sort_keys=True, ensure_ascii=False)

    @staticmethod
    def get_config_file_path(dest):
        return os.path.join(dest, PANDOC_COMPOSE_FILE)
