'''
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of ddserver.

ddserver is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

ddserver is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ddserver.  If not, see <http://www.gnu.org/licenses/>.
'''

import bottle

import formencode

import validators



def validated(cls, target):
  ''' input validation wrapper that takes a validation schema and redirect url
      as parameters. the POST array gets validated, rewritten and returned. if
      validation errors occur, an error message specified by the validator is
      set and a redirect triggered.
  '''
  def wrapper(func):
    def wrapped(*args, **kwargs):
      session = bottle.request.environ.get('beaker.session')

      validator = cls()

      try:
        bottle.request.POST = validator().to_python({k : bottle.request.POST.get(k)
                                                     for k
                                                     in bottle.request.POST})

      except formencode.Invalid, e:
        session['msg'] = ('error', e)

      else:
        func(*args, **kwargs)

      finally:
        session.save()
        bottle.redirect(target)


    return wrapped
  return wrapper



class AddHostnameSchema(formencode.Schema):
  ''' schema for validation of the form for adding a new hostname
  '''
  hostname = formencode.All(validators.ValidHostname(min = 1,
                                                     max = 255),
                            validators.UniqueHostname(),
                            validators.MaxHostnames())
  address = formencode.validators.IPAddress()



class DelHostnameSchema(formencode.Schema):
  ''' schema for validation of the delete action of a hostname
  '''
  hostid = formencode.All(formencode.validators.Int(not_empty = True),
                          validators.HostnameOwner())



class UpdateUserSchema(formencode.Schema):
  ''' schema for validation of the form for editing account information
  '''
  email = formencode.validators.Email()


class UpdatePasswordSchema(formencode.Schema):
  password = validators.SecurePassword(min = 8)
  password_confirm = formencode.validators.String()
  chained_validators = [formencode.validators.FieldsMatch('password',
                                                          'password_confirm')]
