from textwrap import dedent

from pandoc_compose.utils import PANDOC_COMPOSE_FILE


class PandocComposeGenericError(Exception):
    def __init__(self, message=None, *args, **kwargs):
        super().__init__()
        self._message = message
        self.args = args
        self.kwargs = kwargs

    @property
    def message(self):
        if self._message is not None:
            return self._message.format(*self.args, **self.kwargs)
        else:
            return "Unknown PandocComposeGenericError"

    def __str__(self):
        return self.message


class PandocConfigNotFoundError(PandocComposeGenericError):
    ERR_MSG = """
        ERROR: {} does not exist. 
        Please use `dest` argument to point to, or exectute this command in 
        a directory containing a {} file.
    """

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        super().__init__()

    @property
    def message(self):
        return dedent(self.ERR_MSG).format(self.config_file_path, PANDOC_COMPOSE_FILE)


class TaskGlobInvalidSourceFormatError(PandocComposeGenericError):
    ERR_MSG = "{} is currently not a supported {} format; entry {} in section `files` of {} will be ignored"

    def __init__(self, rank, fmt, is_input_fmt=False):
        fmt_nature = "input" if is_input_fmt else "output"
        super().__init__(self.ERR_MSG, fmt, fmt_nature, rank, PANDOC_COMPOSE_FILE),


class TaskGlobInvalidError(PandocComposeGenericError):
    ERR_MSG = "Definition at rank {} is invalid in section `files` of {}{}{}"

    def __init__(self, rank, supplementary_infos="", **kwargs):
        sep = "" if len(supplementary_infos) == 0 else "; "
        super().__init__(self.ERR_MSG, rank, PANDOC_COMPOSE_FILE, sep, supplementary_infos, **kwargs)

    @property
    def message(self):
        return super().message.format(**self.kwargs)


class TaskGlobYouDidEveryWrongError(PandocComposeGenericError):
    ERR_MSG = (
        "All your output format definition for rule {} ({}) are wrong "
        "(seriously, how did you managed to screw up so badly!?)"
    )

    def __init__(self, rank, glob):
        super().__init__(self.ERR_MSG, rank, glob)
