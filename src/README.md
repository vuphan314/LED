<h6>top

# LED ENGINE (SOURCE)

## LED PARSER

### FILES
- `led_lexicon.txt`
- `led_grammar.txt`

### DEMOS
- Windows Command Prompt:
  ```
  D:\repos\LED\src
  $ python led_parser.py ../examples/boolean.led

    ('prog',
      ('constDef',
        ('constN',
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
            ('set'
            )
          )
        )
      )
    )

  ```
- Python:
  ```
  D:\repos\LED\src
  $ py
  Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:18:55) [MSC v.1900 64 bit (AMD64)] on win32
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import led_parser
  >>> led_path = '../examples/boolean.led'
  >>> led_tree = led_parser.parse_file(led_path, quiet=True)
  >>> led_tree
  ('prog', ('constDef', ('constN', ('id', 'c')), ('equiv', ('impl', ('disj', ('conj', ('truth', 'true'), ('truth', 'false')), ('neg', ('eq', ('numl', '1'), ('div', ('numl', '2'), ('numl', '2'))))), ('truth', 'false')), ('uneq', ('atom', '`a'), ('set',)))))

  ```
