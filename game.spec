# -*- mode: python -*-
import os
from os import path
	
block_cipher = None


a = Analysis(['game.py'],
             pathex=['/media/jakov/Podaci/Programming/Python/Ludum Dare/40/game'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
def get_data(folder):
    files = []
    for f in os.listdir(folder):
        f_path = path.join(folder, f)
        if path.isfile(f_path):
            files.append((f_path, f_path, "DATA"))
        else:
            files += get_data(f_path)
    return files

a.datas += get_data(".")
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='disease',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='disease')
