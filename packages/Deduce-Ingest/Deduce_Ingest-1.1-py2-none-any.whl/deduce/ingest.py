# Copyright (c) 2019
# Author: Jeff Weisberg
# Created: 2019-Jul-23 14:05 (EDT)
# Function: python Deduce ingest library

import hashlib
import urllib2
import random
import time
import json
import re

VERSION        = 1.1

COLLECT_URL    = '//lore.deduce.com/p/collect'
EVENT_URL      = "https://event.deduce.com/p/event"    # only https
TIMEOUT        = 1.0
VERHASH        = (hashlib.sha1("python/%s" % VERSION).hexdigest())[0 : 15]

lastt = 0
limit = 0

class Ingest(object):

    def __init__(me, site, apikey, testmode=False):
        """
    Parameters
    ----------
    site : str
      The site id assigned to you by Deduce
    apikey : str
      The secret api key assigned to you by Deduce

    """

        me.site     = site
        me.apikey   = apikey
        me.testmode = testmode


    def html(me, email, use_ssl=None, url="", testmode=False):
        """
        Generate HTML to place on your web page.

        Parameters
        ----------
        email : str
          The user's email address.
          It will be processed and hashed, not used directly.

        """

        data = { 'site': me.site, 'vers': VERHASH }

        if testmode or me.testmode:
            data['testmode'] = True

        if me.__email_valid(email):
            email = email.strip()
            data['ehlm5'] = hashlib.md5(email.lower()).hexdigest()
            data['ehum5'] = hashlib.md5(email.upper()).hexdigest()
            data['ehls1'] = hashlib.sha1(email.lower()).hexdigest()
            data['ehus1'] = hashlib.sha1(email.upper()).hexdigest()
            data['ehls2'] = hashlib.sha256(email.lower()).hexdigest()
            data['ehus2'] = hashlib.sha256(email.upper()).hexdigest()

        if url:
            pass
        elif use_ssl is None:
            url = COLLECT_URL
        elif use_ssl:
            url = 'https:' + COLLECT_URL
        else:
            url = 'http:' + COLLECT_URL

        html = '''<script type="text/javascript">
var dd_info = %s;
</script>
<script type="text/javascript" src="%s" async></script>
''' % (json.dumps(data, indent=2), url)

        return html

    def events(me, evts, timeout=0, backfill=False, url="", testmode=False):
        """
        You can send several related events, by sending an array of event data.

        Parameters
        ----------
        evts : array of dict
          array of event data.
          the events must contain valid email, ip, and event fields.
          any email, email_prev, and cc fields will automatically be processed and hashed.

        Return
        ------
        on success : Nothing
        on fail    : an error string

        """

        if me.__limited():
            return

        post = { 'site': me.site, 'apikey': me.apikey, 'vers': VERHASH }

        if backfill:
            post['backfill'] = True
        if testmode or me.testmode:
            post['testmode'] = True

        post['events'] = list(map(lambda e: me.__fixup_evt(e), evts))

        if not url:
            url = EVENT_URL

        if timeout == 0:
            timeout = TIMEOUT + len(evts) / 10

        # print json.dumps(post)

        # post https
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')

        try:
            res = urllib2.urlopen(req, json.dumps(post), timeout)
        except urllib2.HTTPError as e:
            me.__adjust_fail();
            msg = e.read()
            return "%d - %s" % (e.code, msg)
        except urllib2.URLError as e:
            me.__adjust_fail();
            return e.reason

        me.__adjust_ok()
        return

    def event(me, email, ip, event, additional={}, timeout=0, backfill=False, url="", testmode=False):
        """
        When something interesting happens on your site, tell Deduce.

        Parameters
        ----------
        email : str
          The user's email address.
          It will be processed and hashed, not used directly.
        ip : str
          The user's IP address (v4 or v6)
        event : str
          The evnt type
          Consult with Deduce support to determine the event types.
        additional : dict
          Event data.
          Consult with Deduce support to determine data to send.
          if you pass in 'email_prev' or 'cc' fields, they will be automatically
          processed and hashed, not send directly.

        Return
        ------
        on success : Nothing
        on fail    : an error string

        """

        if not me.__email_valid(email):
            return "invalid email"
        d = additional.copy()
        d['email'] = email
        d['ip']    = ip
        d['event'] = event
        return me.events([d], timeout, backfill, url, testmode)



    def __fixup_evt(me, evt):
        e = evt.copy()
        email = e['email']

        if me.__email_valid(email):
            email = email.strip()
            e['ehls1'] = hashlib.sha1(email.lower()).hexdigest()
            del e['email']

            if not e.has_key('email_provider'):
                e['email_provider'] = email.split('@')[1]

        if e.has_key('email_prev') and me.__email_valid(e['email_prev']):
            e['ehls1_prev'] = hashlib.sha1(e['email_prev'].strip().lower()).hexdigest()
            del e['email_prev']

        if e.has_key('cc'):
            cc = re.sub('[^0-9]', '', e['cc'])
            e['ccs1'] = hashlib.sha1(cc).hexdigest()
            del e['cc']

        return e

    def __email_valid(self,email):
        if re.match(r".+@.+", email):
            return True
        return False

    # rate limit events if they are failing
    def __limited(me):
        global lastt
        global limit

        t = time.time()
        if lastt == 0:
            lastt = t

        dt = t - lastt
        lastt = t
        limit *= 0.999 ** dt
        return random.random() * 100 < limit

    def __adjust_ok(me):
        global limit
        limit -= 5
        if limit < 0:
            limit = 0

    def __adjust_fail(me):
        global limit
        limit = (9 * limit + 100) / 10
        if limit > 100:
            limit = 100


