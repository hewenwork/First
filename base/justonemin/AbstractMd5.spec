# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['F:/Workspace/First/Tools/AbstractMd5.py'],
             pathex=['F:/Workspace/First/Base\\justonemin'],
             binaries=[],
             datas=[],
             hiddenimports=['uvicorn'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='AbstractMd5',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='F:\\Workspace\\First\\Base\\ico.ico')
