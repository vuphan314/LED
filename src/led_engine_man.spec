# -*- mode: python -*-

block_cipher = None

added_files = [
  ('led_lexicon.gen', ''),
  ('led_grammar.gen', '')
]

a = Analysis(['translator.py'],
             pathex=['D:\\git\\LEDtoSLtranslator\\src'],
             binaries=None,
             datas= added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='translator',
          debug=False,
          strip=False,
          upx=True,
          console=True )
