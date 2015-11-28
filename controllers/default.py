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


    return dict(newboxes=db((db.boxes.id > 0) & (db.boxes.privacy_settings == 'Public')).select(
                                        db.boxes.ALL, orderby=db.boxes.date_created, limitby=(0, 5)))
               # biggestboxes=db()

@auth.requires_login()  # Requires user to be logged in
def boxes():
    box_id = request.args(0)
    if box_id is not None:
        return dict(boxes=db(db.boxes.id == box_id).select())
    else:
        return dict(boxes=db(db.boxes.id > 0).select())

@auth.requires_login()  # Requires user to be logged in
def comics():
    comic_id = request.args(0)
    if comic_id is not None:
        return dict(comics=db(db.comics.id == comic_id).select())
    else:
        return dict(comics=db(db.comics.id > 0).select())

@auth.requires_login()  # Requires user to be logged in
def addbox():
    addform = SQLFORM(db.boxes, fields=['name', 'privacy_settings'], buttons=[TAG.button('Add Box', _type="submit")])
    if addform.process().accepted:
        response.flash = 'Box Added'
    elif addform.errors:
        response.flash = 'Errors. See below for details'
    else:
        response.flash = 'Please fill the form'
    return dict(addform=addform)

@auth.requires_login()  # Requires user to be logged in
def addcomic():
    boxes = db((db.boxes.id > 0) & (db.boxes.user_id == auth.user_id)).select()
    addform = SQLFORM(db.comics, buttons=[TAG.button('Add Comic', _type="submit")])
    list_boxes = TR(LABEL('Box'), INPUT(_name='boxes',value=True,_type='drop-down'))
    addform[0].insert(-1,list_boxes)
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

import datetime
def register():
    def post_registration(form): # form accepted
        db.boxes.insert(name="Unfiled", user_id=auth.user.id, date_created=datetime.date.today(), privacy_settings="Public")
        db.commit
    auth.settings.register_onaccept = post_registration
    return dict(form=auth.register())

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
