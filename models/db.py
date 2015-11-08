# Connect database and store in the global variable longboxes
db = DAL('sqlite://longboxes.db')

# -*- coding: utf-8 -*-
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()


## custom user table
db.define_table(
    auth.settings.table_user_name,
    Field('username', length=128, default=''),
    Field('screen_name', length=128, default=''),
    Field('email', length=128, default=''), # required
    Field('password', 'password', length=512,            # required
          readable=False, label='Password'),
    Field('registration_key', length=512,                # required
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,              # required
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,                 # required
          writable=False, readable=False, default=''))

## validators
custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.username.requires = [
    IS_NOT_EMPTY(error_message=auth.messages.is_empty),
    IS_NOT_IN_DB(db, custom_auth_table.username)]
custom_auth_table.screen_name.requires = [
    IS_NOT_EMPTY(error_message=auth.messages.is_empty),
    IS_NOT_IN_DB(db, custom_auth_table.screen_name)]
# custom_auth_table.email.requires = [
#   IS_EMAIL(error_message=auth.messages.invalid_email),
#   IS_NOT_IN_DB(db, custom_auth_table.email)]

auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table

## want to remove email completely from registration
#db.auth_user.email.writable = False # disable edit of email field
#db.auth_user.email.readable = False # remove email from form

## create all tables needed by auth
auth.define_tables(username=True, signature=False)

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True


#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

# @IAPT: Now we need to define a simple set of tables.  There are two tables - 1 for the products, and 1 for the
# features.  The field 'id' will be automatically added to the table as a primary key.  If you want some other field
# to be primary key there are ways to overrride that.  See the Web2Py book for details on how to do that.

# Comic Table: stores details on each comic
db.define_table('comics',
                       Field('cover_image'), # , requires=IS_IMAGE Check if uploaded file is in any of supported image formats
                       Field('title', requires=IS_NOT_EMPTY()),
                       Field('issue_number', requires=IS_NOT_EMPTY()),
                       Field('description', requires=IS_NOT_EMPTY(), widget=SQLFORM.widgets.text.widget),
                       Field('publisher', requires=IS_NOT_EMPTY()),
                       Field('writer', requires=IS_NOT_EMPTY()),
                       Field('artist', requires=IS_NOT_EMPTY()))
                       #Field('comic_id'),

# User Table: stores Longboxes user details
db.define_table('users',
                       Field('user_name', requires=IS_NOT_EMPTY()),
                       Field('screen_name', requires=IS_NOT_EMPTY()),
                       Field('password', requires=IS_NOT_EMPTY(), widget=SQLFORM.widgets.date.widget))
#db.register.user_name.requires=IS_NOT_IN_DB(db,'users.user_name')

# Comic Boxes Table: stores details about the boxes containing collections of comics
db.define_table('boxes',
                       Field('name'),
                       Field('user_id', db.users),
                       Field('date_created'),
                       Field('privacy_settings', requires=IS_IN_SET(['Public', 'Private'])))
                       #Field('box_id'),

# Comics in Boxes Table: stores relation between comics and the boxes they are contained in
db.define_table('comics_in_boxes',
                       Field('comic_id', db.comics),
                       Field('box_id', db.boxes))



# @IAPT: After running your website 1 time, you will automatically have created the above two tables that are empty
# of data.  Be aware - once you start modifying stuff - it can (very rarely) go very wrong.  Migrations will happen automatically,
# and there are several "gotchas" that are documented in the Data Abstraction Layer of Web2Py you should be aware
# of for working with SQLite.