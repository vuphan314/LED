<h6>top</h6>

# LED ENGINE (SOURCE)

## LED PARSER

### FILES
- `led_lexicon.gen`
- `led_grammar.gen`

### DEMO
- Windows Command Prompt:
  ```
  D:\repos\LED\src
  $ python led_parser.py demo/boolean.led
  ('prog',
    ('funDefNoWhere',
      ('formFunExpr',
        ('id', 'c')
      ),
      ('equiv',
        ('impl',
          ('disj',
            ('conj',
              ('truth', 'true'),
              ('truth', 'false')
            ),
            ('neg',
              ('eq',
                ('numl', '1'),
                ('div',
                  ('numl', '2'),
                  ('numl', '2')
                )
              )
            )
          ),
          ('truth', 'false')
        ),
        ('uneq',
          ('atom', '`a'),
          ('setEmpty'
          )
        )
      )
    ),
    ('ledCmnt', 'test:\n\\begin{verbatim}\ncmd:>pp(c)\n"true"\n\\end{verbatim}')
  )
  ```
- Python:
  ```
  D:\repos\LED\src
  $ py
  Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AMD64)] on win32
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import led_parser
  >>> led_parser.parse_file('demo/boolean.led', False)
('prog', ('funDefNoWhere', ('formFunExpr', ('id', 'c')), ('equiv', ('impl', ('disj', ('conj', ('truth', 'true'), ('truth', 'false')), ('neg', ('eq', ('numl', '1'), ('div', ('numl', '2'), ('numl', '2'))))), ('truth', 'false')), ('uneq', ('atom', '`a'), ('setEmpty',)))), ('ledCmnt', 'test:\n\\begin{verbatim}\ncmd:>pp(c)\n"true"\n\\end{verbatim}'))
  ```
