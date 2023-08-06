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
Persona Identity Schema
=======================
"""

from decimal import Decimal

from tendril.schema.base import SchemaControlledYamlFile
from .identity import TendrilIdentity

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class TendrilPersona(TendrilIdentity):
    supports_schema_name = 'TendrilPersona'
    supports_schema_version_max = Decimal('1.0')
    supports_schema_version_min = Decimal('1.0')


class TendrilPersonaFile(TendrilPersona, SchemaControlledYamlFile):
    supports_schema_name = 'TendrilPersonaFile'
    supports_schema_version_max = Decimal('1.0')
    supports_schema_version_min = Decimal('1.0')


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_schema('TendrilPersona', TendrilPersona,
                        doc="Schema for Tendril Persona Definitions")
    manager.load_schema('TendrilPersonaFile', TendrilPersonaFile,
                        doc="Schema for Tendril Persona Definition Files")
