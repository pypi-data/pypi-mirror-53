# -*- mode: python -*-
import sys

projpath = os.path.dirname(os.path.abspath(SPEC))

def get_plugins(list):
    for item in list:
        if item[0].startswith('volbf.plugins') and not (item[0] == 'volbf.plugins' and '__init__.py' in item[1]):
            yield item

exeext = ".exe" if sys.platform.startswith("win") else ""

a = Analysis([os.path.join(projpath, 'vol.py')],
              pathex = [HOMEPATH],
              hookspath = [os.path.join(projpath, 'pyinstaller')])
pyz = PYZ(a.pure)
plugins = Tree(os.path.join(projpath, 'volbf', 'plugins'),
               os.path.join('plugins'))
exe = EXE(pyz,
          a.scripts + [('u', '', 'OPTION')],
          a.binaries,
          a.zipfiles,
          a.datas,
          plugins,
          name = os.path.join(projpath, 'dist', 'pyinstaller', 'volbf' + exeext),
          debug = False,
          strip = False,
          upx = True,
          icon = os.path.join(projpath, 'resources', 'volbf.ico'),
          console = 1)
