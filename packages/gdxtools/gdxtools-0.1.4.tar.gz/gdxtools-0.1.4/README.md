# gdxrw
gdxrw currently contains two classes (gdx_reader and gdx_writer) that enable rapid read and write operations of GAMS GDX files.  These 'helper' classes will allow the user to interface with the GAMS python API through a more intuitive interface (enabled by python dicts).  Examples are provided at https://github.com/boxblox/gdxrw.  

# Requirements
Python 3, GAMS API (manual installation required, see: https://www.gams.com/latest/docs/API_PY_TUTORIAL.html)

An error(s) (such as the ones below) will be thrown if the GAMS API has not been installed:

"ERROR: Could not find a version that satisfies the requirement gams (from gdxtools) (from versions: none)"
"ERROR: No matching distribution found for gams (from gdxtools)"
