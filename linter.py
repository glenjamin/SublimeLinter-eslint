#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by roadhump
# Copyright (c) 2014 roadhump
#
# License: MIT
#

"""This module exports the ESLint plugin class."""

import sublime
import os
from SublimeLinter.lint import NodeLinter


class ESLint(NodeLinter):

    """Provides an interface to the eslint executable."""

    syntax = ('javascript', 'html', 'javascriptnext', 'javascript (babel)', 'javascript (jsx)')
    npm_name = 'eslint'
    cmd = ('eslint', '--format', 'compact', '--stdin', '--stdin-filename', '__RELATIVE_TO_FOLDER__')
    version_args = '--version'
    version_re = r'v(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.20.0'
    regex = (
        r'^.+?: line (?P<line>\d+), col (?P<col>\d+), '
        r'(?:(?P<error>Error)|(?P<warning>Warning)) - '
        r'(?P<message>.+)'
    )
    line_col_base = (1, 0)
    selectors = {
        'html': 'source.js.embedded.html'
    }

    def split_match(self, match):
        """
        Extract and return values from match.

        We override this method to silent warning by .eslintignore settings.

        """

        match, line, col, error, warning, message, near = super().split_match(match)
        if message and message == 'File ignored because of your .eslintignore file. Use --no-ignore to override.':
            return match, None, None, None, None, '', None

        return match, line, col, error, warning, message, near

    def communicate(self, cmd, code=None):
        """Run an external executable using stdin to pass code and return its output."""
        
        window = self.view.window()
        vars = window.extract_variables()
        relfilename = os.path.relpath(self.filename, vars['folder'])

        if '__RELATIVE_TO_FOLDER__' in cmd:
            cmd[cmd.index('__RELATIVE_TO_FOLDER__')] = relfilename
        elif not code:
            cmd.append(self.filename)

        return super().communicate(cmd, code)
