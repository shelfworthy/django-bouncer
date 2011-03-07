from setuptools import setup, find_packages
 
setup(
    name='django-bouncer',
    version='0.2',
    description='Allows you (or users of your site) to invite new people to join',
    author='Chris Drackett',
    author_email='chris@shelfworthy.com',
    url='http://github.com/shelfworthy/django-bouncer',
    packages = [
        "bouncer",
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        # 'Intended Audience :: Designers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Utilities',
    ],
)