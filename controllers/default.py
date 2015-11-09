# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Hello World")
    #return dict(message=T('Welcome to web2py!'))

    return dict(comics=db(db.comics.id > 0).select())

def boxes():
    return dict()

def addbox():
    addform =SQLFORM(db.boxes, fields=['name','privacy_settings'])
    if addform.process().accepted:
        response.flash = 'Box Added'

    elif addform.errors:
        response.flash = 'You fucked up'
    else:
        response.flash = 'Please fill the form'
    return dict(addform=addform)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    #return dict(form=auth())

    loginform = FORM(DIV(LABEL('User name:', _for='user_name')),
                     DIV(INPUT(_name='user_name', requires=IS_NOT_EMPTY(error_message='Please enter user name') )),
                     DIV(LABEL('Password:', _for='password')),
                     DIV(INPUT(_name='password', _type='password', requires=IS_NOT_EMPTY(error_message='Please enter password') )),
                     BR(),
                     DIV(INPUT(_type='submit', _value='Log in')))

    registerform = FORM(DIV(LABEL('User name:', _for='user_name')),
                     DIV(INPUT(_name='user_name', requires=IS_NOT_EMPTY(error_message='Please enter user name')) ),
                     DIV(LABEL('Screen name:', _for='screen_name')),
                     DIV(INPUT(_name='screen_name', requires=IS_NOT_EMPTY(error_message='Please enter screen name') )),
                     DIV(LABEL('Password:', _for='password')),
                     DIV(INPUT(_name='password', _type='password', requires=IS_NOT_EMPTY(error_message='Please enter password') )),
                     DIV(LABEL('Re-enter Password:', _for='re_password')),
                     DIV(INPUT(_name='re_password', _type='password', requires=[IS_NOT_EMPTY(error_message='Please enter password'),
                               IS_EQUAL_TO(request.vars.password,error_message='Passwords do not match')])),
                     BR(),
                     DIV(INPUT(_type='submit', _value='Register')))

    if registerform.accepts(request,session):
        response.flash = 'Product Added'


    elif registerform.errors:
        response.flash = 'Please fix your fuck ups'

    return dict(loginform=auth.login(), form=auth(), registerform=registerform)

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


