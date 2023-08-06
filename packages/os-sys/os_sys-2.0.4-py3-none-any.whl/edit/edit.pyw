try:
    import edit.pyshell
except ImportError:
    # edit is not installed, but maybe pyshell is on sys.path:
    from . import pyshell
    import os
    editdir = os.path.dirname(os.path.abspath(pyshell.__file__))
    if editdir != os.getcwd():
        # We're not in the edit directory, help the subprocess find run.py
        pypath = os.environ.get('PYTHONPATH', '')
        if pypath:
            os.environ['PYTHONPATH'] = pypath + ':' + editdir
        else:
            os.environ['PYTHONPATH'] = editdir
    pyshell.main()
else:
    edit.pyshell.main()
