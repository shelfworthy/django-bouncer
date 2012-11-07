Django Bouncer
==============

This application provides three key features:

* a way for users to sign up for a beta of your site before its launched.
* a way to lock out non-logged in users from pages during a beta period.
* a way for existing users of your site to invite new people to the site

The application takes steps to limit the amount of invite emails a potential member will get.

Installation
------------

To use the invite form, you first need to add bouncer to `INSTALLED_APPS` in your settings file:

```python
    INSTALLED_APPS = (
    #...
    'bouncer',
    )
```

Members Only middleware
-----------------------

If you would also like to prevent non-authenticated users from viewing your site, you can make use of `bouncer.middleware.MembersOnlyMiddleware`. This middleware redirects all views to a specified location if a user is not logged in.

To use the middleware, add it to `MIDDLEWARE_CLASSSES` in your settings file:

```python
    MIDDLEWARE_CLASSES = (
        #...
        'bouncer.middleware.MembersOnlyMiddleware',
    )
```

the middleware uses the following settings from your settings file:





        self.exact_urls = getattr(settings, 'BOUNCER_EXACT_URLS', ['/'])
        self.partial_urls = getattr(settings, 'BOUNCER_PARTIAL_URLS', [])


### BOUNCER_EXACT_URLS

A list of urls that anyone can view. The url needs to exactly match the urls defined in this list.
Examples might include your homepage, your login page, etc.

```python

BOUNCER_EXACT_URLS = [
    '/'
    '/login/'
]

```

### BOUNCER_PARTIAL_URLS

A list of strings that urls should be checked against. This is useful for letting a section of your site be viewed even if it contains more than one url. Any URL containing a string in this list will be show to all visitors.

```python
BOUNCER_EXACT_URLS = [
    '/public/'
]
```

### MEMBERS_ONLY_REDIRECT

Where to redirect people who try and visit a url not on the above list. This url will automattically be added to the `BOUNCER_EXACT_URLS` list.

defaults to `/`

How To Use
==========

Wait List
---------

This app includes a wait list functionality to keep track of people who want access to your site.

You can add users to this list using the `add_to_waitlist` function from `bouncer.functions`.

```python
	list_item, created = add_to_waitlist('some@email.address')
```

This function will return the WaitList object and if it was created or already existed. From the WaitList object you can also check if a user is already a member of the site:

```python
	if list_item.is_user:
		# email is already connected to a user object
	else:
		# email is not connected to a user object
```

This is done by checking existing users of your site. You can use this to notify users trying to join the wait-list that they are already members.
