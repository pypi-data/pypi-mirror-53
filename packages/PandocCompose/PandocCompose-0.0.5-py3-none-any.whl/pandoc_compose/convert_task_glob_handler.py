from pandoc_compose.errors import TaskGlobInvalidError, TaskGlobInvalidSourceFormatError, TaskGlobYouDidEveryWrongError
from pandoc_compose.utils import KNOWN_TARGET_FORMATS, KNOWN_SOURCE_FORMATS, logger
from copy import deepcopy


def normalise(task_glob_definition, rank):
    """
    Normalises the multiple possible structures of the `files` section
    
    Possible cases are:
    - Simplest case:
    ::
        files:
          - "<glob>": <format>

    - Case with multiple formats:
    ::
        files:
          - "<glob>":
            - <target_format1>
            - <target_format2>
            - <target_format3>

    Case with a source format and one target format:
    ::
        files:
          - "<glob>":
            from: <source_format>
            to: <target_format>
    Case with a source format and multiple target format:
    ::
        files:
          - "<glob>":
            from: <source_format>
            to:
            - <target_format1>
            - <target_format2>
            - <target_format3>

    :param task_glob_definition: One item from the `files` section in pandoc-compose.yml
    :param rank: The index of the item
    :return: ::
        {
          "from": source_format,
          "to": [
            target_format1,
            target_format2,
            etc.
          ]
        }
    :type: dict
    """
    if not isinstance(task_glob_definition, dict):
        raise TaskGlobInvalidError(rank)

    glob, formats = list(task_glob_definition.items())[0]

    if isinstance(formats, str):
        result = {"from": None, "to": [formats]}
    elif isinstance(formats, list):
        result = {"from": None, "to": [str(item) for item in formats]}
    elif isinstance(formats, dict):
        for k in ["from", "to"]:
            if k not in formats:
                raise TaskGlobInvalidError(rank, "the key '{key}' is missing", key=k)

        if isinstance(formats["to"], list):
            result = {"from": None, "to": [str(item) for item in formats["to"]]}
        else:
            result = {"from": None, "to": str(formats["to"])}
    else:
        raise TaskGlobInvalidError(rank)

    return __validate({glob: result}, rank)


def __validate(task_glob_definition, rank):
    """
    Validates a normalized task_glob_definition
    """
    new_task_glob_definition = deepcopy(task_glob_definition)
    glob, formats = list(task_glob_definition.items())[0]

    if formats["from"] is not None and not formats["from"] in KNOWN_SOURCE_FORMATS:
        raise TaskGlobInvalidSourceFormatError(rank, formats["from"], True)

    if len(formats["to"]) == 1:
        if KNOWN_TARGET_FORMATS.get(formats["to"][0]) is None:
            raise TaskGlobInvalidSourceFormatError(rank, formats["to"][0])
        else:
            return new_task_glob_definition

    for idx, item in enumerate(formats["to"]):
        if KNOWN_TARGET_FORMATS.get(item) is None:
            logger.warning(
                "%s is currently not a supported output format; "
                "conversion into this format will be ignored for files matching the rule %d (%s)",
                item,
                rank,
                glob,
            )
            new_task_glob_definition[glob]["to"].remove(item)
            pass

    if len(new_task_glob_definition[glob]["to"]) == 0:
        raise TaskGlobYouDidEveryWrongError(rank, glob)

    return new_task_glob_definition
