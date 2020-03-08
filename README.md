Introduction
============

This is a small script, which fetches event invitations (mails with an ics attachment) and merges them into a caldav calendar.

Dependencies
============

* [python-caldav](https://github.com/python-caldav/caldav)
* [python-imapclient](https://github.com/mjs/imapclient)

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
