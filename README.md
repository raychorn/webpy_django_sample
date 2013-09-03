webpy_django_sample
===================

web.py django sample - shows how django can be used with web.py

web.py has a rather weak connection to anything one might wish to call a database; there is no ORM with web.py at-all.


See also: https://pypi.python.org/pypi/django-standalone for some insights into how this was done.

The project template provides support for both mysql and sqlite3 however any django db backend could be used; these are
the ones I chose to use for my sample.

Please be advised some libraries or other portions of this project are missing from this repo; that's life.

This is NOT intended to be a fully functional something you can grab and run without the missing bits, this is however something you can use as a springboard into something that will work, for your specific needs.

What this "is", is something that worked for me albeit with some missing bits you don't need.

Just sweep away the bits you don't have and make this work for your needs - that's what a real software engineer would have to do in any case so get used to the process.

The point of all this is to show you "what" you might have to do to make web.py work with the django ORM - trust me when I tell you this may seem trivial however if you don't know how this should work you can easily run into some django issues related to how django initializes.

Have fun !!!
