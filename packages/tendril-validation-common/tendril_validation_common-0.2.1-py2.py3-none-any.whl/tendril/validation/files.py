#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2016-2019 Chintalagiri Shashank
#
# This file is part of tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
File Validation Patterns (:mod:`tendril.validation.files`)
==========================================================
"""


import os
from tendril.validation.base import ValidatableBase
from tendril.validation.base import ValidationError
from tendril.validation.base import ValidationPolicy


class MissingFileError(ValidationError):
    msg = "Missing File"

    def __init__(self, policy):
        super(MissingFileError, self).__init__(policy)

    def __repr__(self):
        return "<MissingFileError {0} {1}>".format(
            self._policy.context, self._policy.path
        )

    def render(self):
        return {
            'is_error': self.policy.is_error,
            'group': self.msg,
            'headline': "Missing {0}".format(self._policy.context.render()),
            'detail': self._policy.path,
        }


class MangledFileError(ValidationError):
    msg = "Unable to Parse File"

    def __init__(self, policy):
        super(MangledFileError, self).__init__(policy)

    def __repr__(self):
        return "<MangledFileError {0} {1}>".format(
            self._policy.context, self._policy.path
        )

    def render(self):
        return {
            'is_error': self.policy.is_error,
            'group': self.msg,
            'headline': "Mangled {0}".format(self._policy.context.render()),
            'detail': self._policy.path,
        }


class FilePolicy(ValidationPolicy):
    def __init__(self, context, path, is_error):
        super(FilePolicy, self).__init__(context, is_error)
        self.path = path


class ExtantFile(ValidatableBase):
    def __init__(self, filename, basedir, *args, **kwargs):
        self._filename = filename
        self._basedir = basedir
        super(ExtantFile, self).__init__(*args, **kwargs)

    @property
    def filename(self):
        return self._filename

    @property
    def filepath(self):
        return os.path.join(self._basedir, self._filename)

    @property
    def _policy(self):
        return FilePolicy(self._validation_context, self.filepath,
                          is_error=True)

    def _validate(self):
        if not os.path.exists(self.filepath):
            self._validation_errors.add(MissingFileError(self._policy))
        self._validated = True

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self.filename)
