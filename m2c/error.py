class MergeFailedError(Exception):
  """Exception raised if merge failed.
  Attributes:
      errormessage -- errormessage
  """

  def __init__(self, message, ics):
      self.message = message
      self.ics=ics
      
  def __str__(self):
      return "{message} for {ics}".format(message=self.message, ics=self.ics.decode("utf-8"))
