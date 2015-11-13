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
    # response.flash = T("Hello World")
    # return dict(message=T('Welcome to web2py!'))

    return dict(comics=db(db.comics.id > 0).select())


def boxes():
    return dict(boxes=db(db.boxes.id > 0).select())


def comics():
    comic_id = request.args(0)
    if comic_id is not None:
        return dict(comics=db(db.comics.id == comic_id).select())
    else:
        return dict(comics=db(db.comics.id > 0).select())


def addbox():
    addform = SQLFORM(db.boxes, fields=['name', 'privacy_settings'])
    if addform.process().accepted:
        response.flash = 'Box Added'

    elif addform.errors:
        response.flash = 'Errors. See below for details'
    else:
        response.flash = 'Please fill the form'
    return dict(addform=addform)


def addcomic():
    addform = SQLFORM(db.comics)
    if addform.process().accepted:
        response.flash = 'Comic Added'

    elif addform.errors:
        response.flash = 'Errors. See below for details'
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

    return dict(form=auth())


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
