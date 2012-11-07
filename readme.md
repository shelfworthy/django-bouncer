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
        'bouncer.middleware.MembersOnlyMiddleware',
    )

the middleware uses the following settings from your settings file:

### OPEN_TO_PUBLIC_VIEWS

A list of views that anyone can view.
Examples might include your homepage, your login page, etc.

### MEMBERS_ONLY_REDIRECT

Where to redirect people who try and visit a view not on the above list.
Make sure this redirect view *is* on the above list :)
defaults to '/'

How To Use
==========

Wait List
---------

This app includes a wait list functionality to keep track of people who want access to your site.

You can add users to this list using the add_to_waitlist function from bounce.functions.

	list_item, created = add_to_waitlist('some@email.address')

This function will return the WaitList object and if it was created or already existed. From the WaitList object you can also check if a user is already a member of the site:

	if list_item.is_user:
		# email is already connected to a user object
	else:
		# email is not connected to a user object

This is done by checking existing users of your site. You can use this to notify users trying to join the wait-list that they are already members.
