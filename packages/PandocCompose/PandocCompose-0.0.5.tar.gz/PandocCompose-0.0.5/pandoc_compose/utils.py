import logging
from pypandoc import get_pandoc_formats


logging.basicConfig(format="%(asctime)s-%(levelname)s: %(message)s")
logger = logging.getLogger("pandoc-compose")
logger.setLevel(logging.ERROR)

PANDOC_COMPOSE_FILE = "pandoc-compose.yml"
POSSIBLE_OVERRIDES_IN_MD = ["pandoc_options"]
PANDOC_COMPOSE_HASH_FILE_NAME = ".pandoc-compose-hash"
HASH_DEFAULT_SECTION = "DEFAULT"

KNOWN_SOURCE_FORMATS = get_pandoc_formats()[0]

KNOWN_TARGET_FORMATS = {
    "commonmark": ".md",
    "context": ".tex",
    "docbook": ".xml",
    "docbook4": ".xml",
    "docbook5": ".xml",
    "docx": ".docx",
    "epub": ".epub",
    "epub2": ".epub",
    "epub3": ".epub",
    "fb2": ".xml",
    "gfm": ".md",
    "html": ".html",
    "html4": ".html",
    "html5": ".html",
    "icml": ".icml",
    "ipynb": ".py",
    "jats": ".xml",
    "jira": ".txt",
    "json": ".json",
    "latex": ".tex",
    "markdown": ".md",
    "markdown_github": ".md",
    "markdown_mmd": ".md",
    "markdown_phpextra": ".md",
    "markdown_strict": ".md",
    "mediawiki": ".txt",
    "muse": ".muse",
    "native": ".hs",
    "odt": ".odt",
    "opendocument": ".odf",
    "opml": ".opml",
    "plain": ".txt",
    "pdf": ".pdf",
    "pptx": ".pptx",
    "revealjs": ".html",
    "rst": ".rst",
    "rtf": ".rtf",
    "s5": ".html",
    "slideous": ".html",
    "slidy": ".html",
    "texinfo": ".texinfo",
    "textile": ".txt",
    "xwiki": ".txt",
    "zimwiki": ".txt",
}
