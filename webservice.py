__copyright__ = """\
(c). Copyright 2008-2013, Vyper Logix Corp., http://www.VyperLogix.com

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

import os
import sys
import web

import Queue

import json
import urllib

__version__ = '1.0.1'

import logging
from logging import handlers

__SERVICE_NAME__ = 'dirwatcherservice'

LOG_FILENAME = './%s.log' % (__SERVICE_NAME__)

logger = logging.getLogger(__SERVICE_NAME__)
handler = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
logger.addHandler(handler) 
print 'Logging to "%s".' % (handler.baseFilename)

ch = logging.StreamHandler()
ch_format = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(ch_format)
ch.setLevel(logging.INFO)
logger.addHandler(ch)

logging.getLogger().setLevel(logging.INFO)

__imports__ = [f for f in sys.path if (f.replace(os.sep,'/').split('/')[-1].lower().find('django') > -1)]

from vyperlogix.webpy.session import Session
from vyperlogix.misc._utils import timeStampForFileName
from vyperlogix.misc._utils import formattedException

from vyperlogix.misc import _utils

from vyperlogix.lists.ListWrapper import ListWrapper

from vyperlogix.django import django_utils

paths = ListWrapper(sys.path)

for m in __imports__:
    i = paths.findFirstMatching(m)
    if (i > -1):
	del sys.path[i]
	
django_utils.assert_version(1.4)

urls = (
    '/', 'Index',
    '/watcher/(.+)', 'Watcher',
    '/watcher', 'Watcher',
    '/setwindowsagentaddr', 'Nothing',
    '/setwindowsagentaddr/', 'Nothing',
)

### Templates
render = web.template.render('templates', base='base')

web.template.Template.globals.update(dict(
    datestr = web.datestr,
    render = render
))

def notfound():
    return web.notfound("Sorry, the page you were looking for was not found.  This message may be seen whenever someone tries to issue a negative number as part of the REST URL Signature and this is just not allowed at this time.")

class Index:

    def GET(self):
        """ Show page """
        return render.index()

__loggerFileName__ = None

from standalone.conf import settings

class Nothing:
    def POST(self):
	web.header('Content-Type', 'application/json')
	reasons = []
	url = web.ctx.home + web.ctx.path + web.ctx.query
	content = json.dumps(web.ctx.env,cls=CustomJSONENcoder)
	logger.info('%s --> %s %s' % (url,content,web.data()))
	content = json.dumps({'status':''.join(reasons)})
	return content

class Watcher:

    def GET(self, args):
        '''
        '''
        web.header('Content-Type', 'application/json')
        toks = args.split('/')
        app_name = toks[0]
        reasons = ['OK %s %s'%(__SERVICE_NAME__,__version__)]
        content = json.dumps({'status':''.join(reasons)})
        return content

    def POST(self):
	web.header('Content-Type', 'application/json')
	content = json.dumps({'status':reasons})
	return content

app = web.application(urls, globals())
app.notfound = notfound

if (__name__ == '__main__'):
    '''
    python webservice.py 127.0.0.1:9999
    '''
    from optparse import OptionParser
    
    parser = OptionParser("usage: %prog [options] 127.0.0.1:9999")
    parser.add_option('-s', '--syncdb', dest='syncdb', action="store_true", help="should the database be created?")
    parser.add_option('-r', '--repl', dest='repl', action="store_true", help="start a REPL with access to your models")
    parser.add_option('-d', '--dumpdata', dest='dumpdata', action="store_true", help="django dumpdata")
    parser.add_option('-i', '--inspectdb', dest='inspectdb', action="store_true", help="django inspectdb")
    parser.add_option('--dm', '--mysql', dest='mysql', action="store_true", help="mysql db")
    parser.add_option('--ds', '--sqlite3', dest='sqlite3', action="store_true", help="sqlite3 db")
    
    options, args = parser.parse_args()

    DOMAIN_NAME = django_utils.socket.gethostname()
    print '1.DOMAIN_NAME=%s' % (DOMAIN_NAME)
	
    if (not options.mysql) and (not options.sqlite3):
	raise AssertionError('Either mysql or sqlite3 is required.')

    __database_name__ = 'dirwatcherservicedb'
    
    if options.mysql:
	print 'INFO: Using mysql... Database "%s".' % (__database_name__)
	if (DOMAIN_NAME in ['HPDV7-6163us']):
	    DATABASES = {
		'default': {
		    'ENGINE': 'django.db.backends.mysql',
		    'NAME': __database_name__,
		    'USER' : 'root',
		    'PASSWORD' : 'your-password-goes-here',
		    'HOST' : '127.0.0.1',
		    'PORT' : '3306',
		}
	    }
    elif options.sqlite3:
	__database_name__ = '%s/%s.sqlite' % (os.path.dirname(sys.argv[0]).replace(os.sep,'/'),__database_name__)

	print 'INFO: Using sqlite3... Database "%s".' % (__database_name__)
	if (DOMAIN_NAME in ['HPDV7-6163us']):
	    DATABASES = {
		'default': {
	            'ENGINE': 'django.db.backends.sqlite3',
		    'NAME': __database_name__,
		}
	    }

    settings = settings(
        DATABASES = DATABASES
    )
    
    import models

    from django.core.management import call_command
    if options.syncdb:
	# run a simple command - here syncdb - from the management suite
	call_command('syncdb')
	sys.exit(1)
    elif options.repl:
	# start the shell, access to your models through import standalone.models
	call_command('shell')
	sys.exit(1)
    elif options.dumpdata:
	call_command('dumpdata')
	sys.exit(1)
    elif options.inspectdb:
	call_command('inspectdb')
	sys.exit(1)

    has_binding = any([_utils.__regex_valid_ip_and_port__.match(arg) for arg in args])
    if (not has_binding):
	sys.argv.append('127.0.0.1:9999')

    def __init__():
	logger.info('%s %s started !!!' % (__SERVICE_NAME__,__version__))
	flush_handlers()
        app.run()

    __init__()    

	
