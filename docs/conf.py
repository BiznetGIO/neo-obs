import os
import sys

sys.path.insert(0, os.path.abspath("../"))

import obs


project = "neo-obs"
copyright = "2019, BiznetGio"
author = "BiznetGio"
version = obs.__version__
release = obs.__version__
templates_path = ["_templates"]
extensions = ["sphinx.ext.autodoc", "sphinx.ext.doctest"]
source_suffix = ".rst"
master_doc = "index"
pygments_style = "sphinx"
html_theme = "alabaster"
html_logo = "_static/img/flex.svg"
html_static_path = ["_static"]
pygments_style = "sphinx"
