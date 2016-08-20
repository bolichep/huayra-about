from distutils.core import setup

setup(name = "huayra-about",
      version = "0.1.1",
      description = "Acerca de Huayra",
      author = "Pedro Boliche",
      author_email = "bolichep@gmail.com",
      url = "https://github.com/bolichep/huayra-about",
#      py_modules = ["huayra-about"],
#      scripts = ["huayra-about"],
      data_files = [ ("share/huayra-about", ["src/huayra-about.py","src/rasti.py","src/markup.py","src/info_table.py"]),
                     ("share/huayra-about/media", ["src/media/huayra-menu-huayra.svg","src/media/huayra-about-background.svg"]),
                     ("share/huayra-about/plugins", ["src/plugins/__init__.py","src/plugins/01versiones.py","src/plugins/02arch.py","src/plugins/03cpu_mem.py","src/plugins/04kernel.py","src/plugins/05link.py"]),
                     ("share/applications", ["huayra-about.desktop"]),
                     ("share/icons/hicolor/scalable/apps",["src/media/huayra-about.svg"]),
                     ("share/man/man1", ["huayra-about.1"]) ] )


