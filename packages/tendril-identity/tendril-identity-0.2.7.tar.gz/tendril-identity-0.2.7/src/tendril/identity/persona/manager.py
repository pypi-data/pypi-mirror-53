#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2019 Chintalagiri Shashank
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
Tendril Persona Manager
=======================
"""

import os
import glob

from tendril import schema
from tendril.schema.identity_persona import TendrilPersona
from tendril.config import PRIMARY_PERSONA

from tendril.config import instance_path
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class IdentityManager(object):
    def __init__(self, prefix):
        self._prefix = prefix
        self._identities_loaded = {}
        self._load_identities()

    @property
    def _placeholder_persona(self):
        return TendrilPersona({'ident': 'PLACEHOLDER',
                               'name': 'Placeholder Identity'})

    @property
    def primary_persona(self):
        if PRIMARY_PERSONA:
            return self._identities_loaded[PRIMARY_PERSONA]
        else:
            if len(self._identities_loaded.keys()) == 1:
                return self._identities_loaded[
                    self._identities_loaded.keys()[0]
                ]
            return self._placeholder_persona

    def _load_identities(self):
        _persona_folder = instance_path('identity')
        logger.debug("Loading personas from {0}".format(_persona_folder))
        candidates = glob.glob(os.path.join(_persona_folder, '*.yaml'))
        for candidate in candidates:
            persona = schema.load(candidate)
            if not isinstance(persona, TendrilPersona):
                continue
            logger.debug("Installing persona {0} from {1}"
                         "".format(persona.ident, candidate))
            self._identities_loaded[persona.ident] = persona
        logger.debug("Done loading personas from {0}".format(_persona_folder))

    def __getattr__(self, item):
        if item == '__all__':
            return list(self._identities_loaded.keys())
        if item == '__path__':
            return self.__module__.__path__
        return self._identities_loaded[item]
