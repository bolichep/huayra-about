from distutils.core import setup

setup(name = "huayra-about",
      version = "0.1",
      description = "Acerca de Huayra",
      author = "Pedro Boliche",
      author_email = "bolichep@gmail.com",
      url = "https://github.com/bolichep/huayra-about",
#      py_modules = ["huayra-about"],
#      scripts = ["huayra-about"],
      data_files = [ ("share/huayra-about", ["huayra-menu-huayra.svg","huayra-about.py"]),
                     ("share/applications", ["huayra-about.desktop"]),
                     ("share/man/man1", ["huayra-about.1"]) ] )
