# setup.py
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\nosov\\Anaconda3\\pkgs\\python-2.7.13-0\\tcl\\tcl8.5"
os.environ['TK_LIBRARY'] = "C:\\Users\\nosov\\Anaconda3\\pkgs\\python-2.7.13-0\\tcl\\tk8.5"
#C:\Users\nosov\Anaconda3\pkgs\python-3.5.2-0


from cx_Freeze import setup, Executable
#build_exe_options = {"packages": ["pandas", "pyparsing"]}
setup(
    name = "21",
    version = "0.1",
    description = "Adventum",
    #options = {"build_exe": build_exe_options},
    executables = [Executable("evaluation_of_sources.py")]
)