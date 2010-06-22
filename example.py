from ExpressionParser import ExpressionParser


class ExampleExpressionParser(ExpressionParser):
    # syntax definition for the parser
    # ! order is important
    syntax = [
                # group, eg: "(...)"
                { 'start': '\\s*\(',
                  'end': '\)\\s*',
                  'type': 'group'
                },

                # propval, eg: "hasNotes:true"
                # with optional NOT modifier
                { 'start': '\\s*([Nn][Oo][Tt])?\\s*([a-z][a-zA-Z]*): *("(.+?)"|[^ ()]+)\\s*',
                  'type': 'propval',
                  'create': lambda m: (m.group(2), m.group(4) or m.group(3), m.group(1))
                },

                # operator, eg: "AND", "OR"
                { 'start': '\\s*(?i)(AND|OR)\\s*', # case insensitive
                  'type': 'operator',
                  'create': lambda m: m.group(1)
                },

                # text
                # with optional NOT modifier
                # if nothing else matched - match all characters until special
                # character found
                { 'start': '\\s*([Nn][Oo][Tt])?\\s*([ ()]?[^ ()]*)',
                  'type': 'text',
                  'create': lambda m: (m.group(2), m.group(1))
                }
             ]


#
# Usage example
#
query = "(list:Personal OR list:Work) AND NOT due:tomorrow"
parser = ExampleExpressionParser()
print parser.parse(query)

