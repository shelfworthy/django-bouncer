Django Bouncer
==============

This application provides three key features:

* a way for users to sign up for a beta of your site before its launched.
* a way to lock out non-logged in users from pages during a beta period.
* a way for existing users of your site to invite new people to the site

The application takes steps to limit the amount of invite emails a potential member will get.

Installation
------------

To use the invite form, you first need to add bouncer to INSTALLED_APPS in your settings file:

    INSTALLED_APPS = (
    #...
    'bouncer',
    )

Members Only middleware
-----------------------

If you would also like to prevent non-authenticated users from viewing your site, you can make use of bouncer.middleware.MembersOnly. This middleware redirects all views to a specified location if a user is not logged in.

To use the middleware, add it to MIDDLEWARE_CLASSSES in your settings file:

    MIDDLEWARE_CLASSES = (
        #...
        'bouncer.middleware.MembersOnly',
    )

the middleware uses the following settings from your settings file (if they exist):

### OPEN_TO_PUBLIC_VIEWS

A list of views that anyone can view.
Examples might include your homepage, your login page, etc.

### MEMBERS_ONLY_REDIRECT

Where to redirect people who try and visit a view not on the above list.
Make sure this redirect view *is* on the above list :)
defaults to '/'

How To Use
==========

