# Simple expression parser in pure Python
# Authors: Andrey Popelo <andrey@popelo.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import re


class ExpressionParser(object):
    """Very simple but configurable parser for parsing different expressions.

    Syntax definition should be defined in subclass.
    
    Call parse() method with input string as a parameter and it will return a
    tree which contains parsed data."""

    # syntax definition for the parser
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
                #
                #
                # Example syntax definition is listed below. Parser with this
                # syntax definition can parse simple expressions, which look
                # like:
                #   "prop1:val1"
                #   "prop1:val1 AND prop2:val2 OR prop3:val3"
                #   "(prop1:val1 AND NOT (prop2:val2 OR prop3:val3)) AND prop4:val4"
                #   ...
                #
                #  # group, eg: "(...)"
                #  { 'start': '\\s*\(', # cut opening bracket and leading white space
                #    'end': '\)\\s*',   # cut closing bracket and following white space
                #    'type': 'group'
                #  },
                #
                #  # propval, eg: "prop1:val1"
                #  # with optional NOT modifier
                #  { 'start': '\\s*(NOT)?\\s*([a-zA-Z0-9]+):\\s*([^ ()]+)\\s*',
                #    'type': 'propval',
                #    'create': lambda m: {"modifier":m.group(1), "prop":m.group(2), "val":m.group(3)}
                #  },
                #
                #  # operator, eg: "AND", "OR"
                #  { 'start': '\\s*(AND|OR)\\s*',
                #    'type': 'operator',
                #    'create': lambda m: m.group(1)
                #  },
                #
                #  # text - all other text
                #  { 'start': '[ ()]?[^ ()]*', # match all characters until special character found
                #    'type': 'text'
                #  }
             ]

    def parse(self, text):
        self.text = text.strip()

        self.tokens_stack = []
        self.parent_stack = []

        while self.text:
            # check if one of end regexps matches
            if self._search_end_patterns():
                continue

            # check if one of start regexps matches
            if self._search_start_patterns():
                continue

        return self.tokens_stack

    def _search_start_patterns(self):
        if self.parent_stack:
            parent_item = self.parent_stack[-1]
        else:
            parent_item = None

        for syntax_def in self.syntax:
            match = self._match_and_cut(syntax_def['start'])

            if match:
                type = syntax_def['type']

                if "end" in syntax_def:
                    item = {'type':type, 'end':syntax_def['end'], 'value':[]}
                    self.parent_stack.append(item)
                else:
                    if 'create' in syntax_def:
                        value = syntax_def['create'](match)
                    else:
                        value = match.group(0)

                    item = {'type': type, 'value': value}

                # if it has a parent, add it to parent
                if parent_item:
                    stack = parent_item['value']
                else:
                    stack = self.tokens_stack

                stack.append(item)

                return True

        return False

    def _search_end_patterns(self):
        # check if one of end regexps matches
        for item in self.parent_stack[::-1]:
            if self._match_and_cut(item['end']):
                self.parent_stack.pop()
                return True

        return False

    def _match_and_cut(self, pattern):
        match = re.match(pattern, self.text)

        if match:
            # cut matched text
            self.text = self.text[len(match.group(0)):]

        return match
