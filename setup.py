import sys
import os
from cx_Freeze import setup, Executable

# RONAN FIX Qt: no image when execute application
# cx_Freeze do not add imageformats directory,
imageformats_DIR = os.path.join(
    os.path.dirname(sys.executable), 'Library', 'plugins', 'imageformats')

# GUI applications require a different base on Windows (the default is for a
# console application).

base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable(
    script="lsi_ui/lsi_ui.py",
    base=base,
    shortcutDir="DesktopFolder",
)

# Dependencies are automatically detected, but it might need fine tuning.

excludes = ["tkinter", "collections.abc"]
#FIX NMB
includes = []
include_files = ["lsi\LogLsi.py",
                 imageformats_DIR]

packages = ["py_baTools",
            "lsi_ui",
            ]

build_exe_options = {
    "packages": ["os"],
    "excludes": excludes,
    "includes": includes,
    "include_files": include_files,
    "packages": packages,
}

setup(name="Lsi",
      version="1.0",
      description="Lsi application!",
      options={"build_exe": build_exe_options},
      executables=[exe],
      package_data={'': ["py_baTools\image\*"]}
      )
