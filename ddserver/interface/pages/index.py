'''
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of ddserver.

ddserver is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

ddserver is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with ddserver. If not, see <http://www.gnu.org/licenses/>.
'''

import os

import bottle

from ddserver.web import route

from ddserver.utils.deps import require



@route('/static/<path:path>', method = 'GET')
def get_static(path):
  ''' Provides a route to static files (like css, images, etc). '''

  return bottle.static_file(path,
                            os.path.join(os.getcwd(),
                                         'ddserver',
                                         'resources',
                                         'web'))



@route('/', method = 'GET')
@require(templates = 'ddserver.interface.template:TemplateManager')
def get_index(templates):
  ''' Display the index page. '''

  return templates['index.html']()
