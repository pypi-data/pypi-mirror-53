import logging
import os
from io import StringIO
from json import JSONDecodeError
from panflute import load as pf_load, dump as pf_dump
from pypandoc import convert_file, convert_text
from time import time

from pandoc_compose.utils import KNOWN_TARGET_FORMATS, POSSIBLE_OVERRIDES_IN_MD, logger


class ConvertTaskCallback:
    def __init__(self, pandoc_compose_config, file_path, target_formats, source_format=None):
        self.file_path = file_path
        self.target_formats = target_formats
        self.pandoc_compose_config = pandoc_compose_config
        self.pandoc_config = pandoc_compose_config.pandoc_config
        self.source_format = source_format

    def __call__(self, *args, **kwargs):
        for target_format in self.target_formats:
            self.__convert_one_target(target_format)

    def __convert_one_target(self, target_format):
        try:
            logger.info("Starting converting %s to %s", self.file_path, target_format)
            if logger.isEnabledFor(logging.DEBUG):
                self.__convert_file_timed(target_format)
            else:
                self.__convert_file(target_format)
            logger.info("Finished converting %s to %s", self.file_path, target_format)
        except Exception as e:
            rest = (
                ""
                if logger.isEnabledFor(logging.WARNING)
                else "\n    | (Try to increase the verbosity to see error message)"
            )
            logger.error("Pandoc failed to convert %s to %s%s", self.file_path, target_format, rest)
            logger.warning("Error was:\n    | %s", e)

    def __convert_file(self, target_format):
        ast = self.__get_pandoc_ast()
        ast_meta = ast.get_metadata(builtin=True).copy()

        individual_overrides = ast_meta.get("pandoc_compose", None)
        new_config = {}
        if isinstance(individual_overrides, dict):
            for key in POSSIBLE_OVERRIDES_IN_MD:
                if key == "pandoc_options":
                    # Pandoc's `smart` markdown extension replaces double dashes to half-em-dashes which breaks cli opts
                    new_config[key] = [x.replace("–", "--").replace("—", "---") for x in individual_overrides.get(key)]
                else:
                    new_config[key] = individual_overrides.get(key)
            ast_meta.pop("pandoc_compose")

        new_config["pandoc"] = ast_meta

        self.pandoc_config = self.pandoc_config.merge(new_config)

        if logger.isEnabledFor(logging.DEBUG):
            json_str = str(self.pandoc_config).replace("\n", "\n    | ")
            logger.debug("pandoc-compose configuration for %s:\n    | %s", self.file_path, json_str)

        ast.metadata = self.pandoc_config.pandoc

        extension = KNOWN_TARGET_FORMATS.get(target_format, ".txt")
        new_name = os.path.splitext(self.file_path)[0] + extension
        extra_args = self.pandoc_config.pandoc_options

        if target_format == "latex":
            # Produce standalone fully compilable LaTeX
            extra_args.append("--standalone")

        with StringIO() as pandoc_ast_json:
            pf_dump(ast, pandoc_ast_json)
            convert_text(
                pandoc_ast_json.getvalue(), target_format, extra_args=extra_args, format="json", outputfile=new_name
            )

    def __convert_file_timed(self, target_format):
        start_time = time()
        self.__convert_file(target_format)
        end_time = time()
        sec_elapsed = end_time - start_time

        h = int(sec_elapsed / (60 * 60))
        m = int((sec_elapsed % (60 * 60)) / 60)
        s = sec_elapsed % 60.0

        h_str = "" if h == 0 else "{}h".format(h)
        m_str = "" if m == 0 else "{:>02}m".format(m)
        s_str = "" if s == 0 else "{:>05.2f}s".format(s)

        end_msg = "".join([h_str, m_str, s_str])

        logger.debug("Processing %s took %s to execute", self.file_path, end_msg)

    def __get_pandoc_ast(self):
        """Convert a file to a pandoc AST

        This is usefull to apply transformations to files before converting them.
        In particular, metadata transformations can be applied.

        See `Pandoc filters <https://pandoc.org/filters.html>`_

        :param file: Path to file
        :type: str
        :return: Pandoc AST in the form of a parsed JSON
        :type: panflute.Doc
        """
        json_str = convert_file(self.file_path, "json", self.source_format) if os.path.exists(self.file_path) else "{}"
        try:
            return pf_load(StringIO(json_str))
        except JSONDecodeError:
            return pf_load(StringIO("{}"))
