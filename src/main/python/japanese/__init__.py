# -*- coding: utf-8 -*-

# Copyright (C) 2013  Alex Yatskov
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

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from .deinflect import Deinflector
from .dictionary import Dictionary
from .translate import Translator

def initLanguage():
    appctxt = ApplicationContext()
    return Translator(
        Deinflector(appctxt.get_resource('yomichan/deinflect.json')),
        Dictionary(appctxt.get_resource('yomichan/dictionary.db'))
    )
