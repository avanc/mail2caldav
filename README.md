Introduction
============

This is a small script, which fetches event invitations (mails with an ics attachment) and merges them into a caldav calendar.
The intention is to send invitations to a special mail address and all events are collected in a calendar.

Details
-------

mail2caldav fetches all calendar events (ics files) from mails in the Inbox of an IMAP account. For each ics file it gets the UID and searches for an existing event with the same UID on the caldav server. If an event exists, it is merged with the update. Otherwise, a new event ist created on the caldav server.
Also, there's an option that allows you to specify the email scanning depth in days, especially if you're running the application regularly. By default, entire mailbox will be scanned, which can take time and potentially cause memory errors.
It's recommended to set the scanning depth to 2 days, like this:
```shell
mail2caldav --scan-depth 2

mail2caldav should be executed reguarly (e.g. via CRON) search for new messages.

Nextcloud
---------
Although mail2caldav should work with any caldav server, it was heavily tested with [Nextcloud](https://nextcloud.com)'s caldav server. Therefore some hints on how mail2caldav can be used with Nextcloud.

Instead of give you password to mail2caldav (which won't work if 2FA is activated), create a new app password (Settings->Security: "Create new app password") within the Nextcloud web interface. This password can be used in combination with your username to login to the caldav server.

If events shall be added to different calendars, the easisest way is to create a new Nexcloud user account just mail2dav und just share calendars (writeable) with that new user.


Dependencies
============

* [python-caldav](https://github.com/python-caldav/caldav)
* [python-imapclient](https://github.com/mjs/imapclient)
* [python-icalendar](https://github.com/collective/icalendar)

Installation
============

    git clone https://github.com/avanc/mail2caldav.git
    cd mail2caldav
    python setup.py install
    cp config/m2c.conf ~/.m2c.conf

Modify ~/.m2c.conf to your needs.

Usage
=====

mail2caldav
