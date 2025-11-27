import os, sys, traceback
print('cwd:', os.getcwd())
print('sys.path[0]:', repr(sys.path[0]))
print('\nPYTHONPATH entries:')
for p in sys.path:
    print(p)
print('\n--- try import app ---')
try:
    import app
    print('imported app, has attribute app:', hasattr(app, 'app'))
except Exception:
    traceback.print_exc()
