# Copyright (C) 2020 Sven Klomp (mail@klomp.eu)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

import logging
logger = logging.getLogger(__name__)

import email
from imapclient import IMAPClient

from . import ical_tools

class MailFetcher(object):
  def __init__(self, host, user, password, folder_inbox, folder_archive, folder_error):
    self.server=IMAPClient(host)
    self.server.login(user, password)
    self.folder_inbox=folder_inbox
    self.folder_archive=folder_archive
    self.folder_error=folder_error
    
    if self.server.folder_exists(self.folder_archive):
      logger.info("Archive folder '{folder}' exists.".format(folder=self.folder_archive))
    else:
      self.server.create_folder(self.folder_archive)
      logger.info("Archive folder '{folder}' created.".format(folder=self.folder_archive))
    
    if self.server.folder_exists(self.folder_error):
      logger.info("Error folder '{folder}' exists.".format(folder=self.folder_error))
    else:
      self.server.create_folder(self.folder_error)
      logger.info("Error folder '{folder}' created.".format(folder=self.folder_error))


  def findIcs(self, rawmail):
    email_message = email.message_from_bytes(rawmail)
    for part in email_message.walk():
      logger.debug(part.get_content_type())
      if ("text/calendar" in part.get_content_type()):
        logger.info("Found calendar event in mail from {sender} with subject '{subject}'.".format(sender=email_message.get('From'), subject=email_message.get('Subject')))
        
        return ical_tools.parse(part.get_payload(decode=True))
    
  def getIcs(self):
    select_info = self.server.select_folder(self.folder_inbox)
    logger.debug("{num_mails} messages in folder {folder}.".format(num_mails=select_info[b'EXISTS'], folder=self.folder_inbox))
    
    ics_list=[];
    
    messages = self.server.search('ALL')
    for message_uid, message_data in self.server.fetch(messages, 'RFC822').items():
      logger.debug("Found message with id {id}".format(id=message_uid))
      ics = self.findIcs(message_data[b'RFC822'])
      if (ics):
        ics_list.append((message_uid, ics))
    return ics_list



  def archiveMessage(self, uid, error=False):
    folder=self.folder_archive
    if error:
      folder=self.folder_error
      
    self.server.move([uid], folder)
    logger.info("Message with UID {uid} moved to folder {folder}".format(uid=uid, folder=folder))
    
