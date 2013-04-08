Simple configurable expression parser in pure Python
====================================================

Authors: Andrey Popelo <andrey@popelo.com>


Usage
-----

1. Subclass ExpressionParser and define a syntax.
2. Instantiate it and call parse() method.

The syntax definition for the parser looks like this::

    # (!) order is important
    syntax = [
                # This is a token definition, it can contain the following
                # fields:
                #
                #  {
                #    'start': <regex>,  # regexp wich matches a start of a token
                #
                #    'end':   <regex>,  # (optional) regexp which matches end of
                #                       # a token
                #
                #    'type':  <string>, # type (or name) of a token
                #
                #    'create': <fnc>    # (optional) function which will be
                #  }                    # called after text which mathes this
                #                       # type of token was found.
                #                       # Function should accept one parameter
                #                       # which is a MatchObject object and
                #                       # return a result which will be stored
                #                       # in a resulting tree


                # Example syntax definition is listed below. Parser with this
                # syntax definition can parse simple expressions, which look
                # like:
                #   "prop1:val1"
                #   "prop1:val1 AND prop2:val2 OR prop3:val3"
                #   "(prop1:val1 AND NOT (prop2:val2 OR prop3:val3)) AND prop4:val4"
                #   ...
                #

                # group, eg: "(...)"
                { 'start': '\\s*\(', # cut opening bracket and leading white space
                  'end': '\)\\s*',   # cut closing bracket and following white space
                  'type': 'group'
                },
                
                # propval, eg: "prop1:val1"
                # with optional NOT modifier
                { 'start': '\\s*(NOT)?\\s*([a-zA-Z0-9]+):\\s*([^ ()]+)\\s*',
                  'type': 'propval',
                  'create': lambda m: {"modifier":m.group(1), "prop":m.group(2), "val":m.group(3)}
                },
                
                # operator, eg: "AND", "OR"
                { 'start': '\\s*(AND|OR)\\s*',
                  'type': 'operator',
                  'create': lambda m: m.group(1)
                },
                
                # text - all other text
                { 'start': '[ ()]?[^ ()]*', # match all characters until special character found
                  'type': 'text'
                }
             ]

See code examples in example.py file.


License
-------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


More info
---------

See a blog post about ExpressionParser[1].

[1] - http://popelo.com/blog/2010-05-31-simple-expression-parser-in-python/
