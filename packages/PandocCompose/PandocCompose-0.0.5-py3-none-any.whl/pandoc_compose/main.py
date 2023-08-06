import os
import sys
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser
from fnmatch import fnmatch
from glob import iglob
from io import StringIO
from pypandoc import get_pandoc_path
from textwrap import dedent

from pandoc_compose.errors import PandocComposeGenericError, PandocConfigNotFoundError
from pandoc_compose.utils import KNOWN_TARGET_FORMATS, PANDOC_COMPOSE_FILE, HASH_DEFAULT_SECTION, logger
from pandoc_compose.convert_task_callback import ConvertTaskCallback
from pandoc_compose.pandoc_config import PandocConfig
from pandoc_compose.pandoc_compose_config import PandocComposeConfig
from pandoc_compose import version, name


def __convert_files(pandoc_compose_config):
    callbacks = []
    file_paths = []
    found_files = iglob(os.path.join(pandoc_compose_config.destination, "**"), recursive=True)

    has_pandoc_compose_config_changed = __has_pandoc_compose_config_changed(pandoc_compose_config)

    for file_path in found_files:
        formats = __find_target_format(file_path, pandoc_compose_config)
        if formats is not None:
            source_format, target_formats = formats["from"], formats["to"]
            file_paths.append(file_path)

            shoud_convert = __shoud_convert_file(file_path, pandoc_compose_config)
            if has_pandoc_compose_config_changed or shoud_convert:
                cb = ConvertTaskCallback(pandoc_compose_config, file_path, target_formats, source_format)
                callbacks.append(cb)
            elif not has_pandoc_compose_config_changed:
                logger.info("%s hasen't changed since last exectution; it won't be processed", file_path)

    if pandoc_compose_config.force:
        logger.info("pandoc-compose is executing in force mode; all files will be processed")
    elif len(callbacks) > 0 and has_pandoc_compose_config_changed:
        logger.info("%s has changed since last process; all files will be processed", PANDOC_COMPOSE_FILE)
    elif len(file_paths) == 0:
        logger.info("No file to process found")

    with ThreadPoolExecutor(max_workers=16) as executor:
        for cb in callbacks:
            executor.submit(cb)

    # Update all SHA256 of the files
    hash_config = {
        PANDOC_COMPOSE_FILE: PandocComposeConfig.get_file_hash(pandoc_compose_config.pandoc_config.config_file_path)
    }

    for file_path in file_paths:
        relative_file_path = file_path.replace(pandoc_compose_config.destination, "")
        hash_config[relative_file_path] = PandocComposeConfig.get_file_hash(file_path)

    with open(pandoc_compose_config.hash_file_path, "w") as pcf:
        cp = ConfigParser()
        # https://stackoverflow.com/questions/19359556/configparser-reads-capital-keys-and-make-them-lower-case
        cp.optionxform = str
        cp[HASH_DEFAULT_SECTION] = hash_config
        cp.write(pcf)
        logger.debug("New file hash written in %s", pandoc_compose_config.hash_file_path)

    logger.info("Finished")


def __find_target_format(file_path, pandoc_compose_config):
    if not os.path.isfile(file_path):
        return None

    for item in pandoc_compose_config.pandoc_config.files:
        glob, formats = list(item.items())[0]
        if fnmatch(file_path, os.path.join(pandoc_compose_config.destination, glob)):
            return formats
    else:
        return None


def __has_pandoc_compose_config_changed(pandoc_compose_config):
    pandoc_config_computed_file_hash = pandoc_compose_config.hash_config.get(PANDOC_COMPOSE_FILE)
    return pandoc_config_computed_file_hash != pandoc_compose_config.pandoc_config_file_hash


def __shoud_convert_file(file_path, pandoc_compose_config):
    if pandoc_compose_config.force:
        return True

    # File won't be converted if both it and pandoc-compose configuration haven't been modified
    # We determine that a file was nt modified by comparing it's computed SHA256 hash and
    # the one that was stored in .pandoc-compose-hash
    file_relative_path = file_path.replace(pandoc_compose_config.destination, "")
    file_hash = PandocComposeConfig.get_file_hash(file_path)

    pandoc_config_computed_file_hash = pandoc_compose_config.hash_config.get(file_relative_path, None)
    return file_hash != pandoc_config_computed_file_hash


def __check_install():
    # Check Python version
    if sys.version_info < (3, 5):
        logger.fatal("This scripts only support Python>=3.5, current version is %s", sys.version_info)
        exit(1)

    # Checks pandoc install
    try:
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        get_pandoc_path()
    except OSError:  # TODO: handle download pandoc switch
        logger.error(
            dedent(
                """
                No pandoc was found: either install pandoc and add it to your PATH variable.
                See http://johnmacfarlane.net/pandoc/installing.html for installation options
                """
            )
        )
        exit(1)
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


def main():
    __check_install()

    description = dedent(
        """
        Process every markdown file in a directory and convert it into PDF

        `pandoc-compose` is a wrapper around pandoc for batch processing multiple Markdown documents 
        in a directory while mutualising documents metadata in a single `{0}` file.

        Any Pandoc metadata variable (see https://pandoc.org/MANUAL.html#metadata-variables) can be set in 
        `{0}`. Every metadata variable will be incuded in every Markdown file during conversion 
        unless it is overriden in the file itself.
        """
    ).format(PANDOC_COMPOSE_FILE)

    parser = ArgumentParser(description=description)

    parser.add_argument("--version", action="version", version="{} {}".format(name, version))

    parser.add_argument(
        "dest",
        metavar="dest",
        type=str,
        nargs="?",
        default=os.getcwd(),
        help="Destination (defaults to current directory)",
    )

    parser.add_argument("--verbose", "-v", action="count", help="Verbose mode (use -vv and -vvv to increase)")

    parser.add_argument(
        "--timeout",
        "-t",
        action="store",
        help=dedent(
            """
            Sets a timeout for each file processing. 
            If a file cannot be converted after the timeout is elapsed, the convertion is aborted.
            This parameters takes a interger value in seconds by default. 'h', 'm' and 's' suffix also work.
            Examples: -t 10s, -t 1000
            """
        ),
    )

    parser.add_argument(
        "--force", "-f", action="store_true", help="Forces the conversion of every file whether they've changed or not"
    )

    try:
        reminder = sys.argv.index("--")
        remaining = sys.argv[(reminder + 1) :]
        sys.argv = sys.argv[:reminder]
        cli_args = parser.parse_args()
    except ValueError:
        cli_args = parser.parse_args()
        remaining = []

    try:
        __convert_files(PandocComposeConfig(cli_args, *remaining))
    except PandocComposeGenericError as pce:
        logger.error(pce.message)
        parser.print_help(sys.stderr)


if __name__ == "__main__":
    main()
