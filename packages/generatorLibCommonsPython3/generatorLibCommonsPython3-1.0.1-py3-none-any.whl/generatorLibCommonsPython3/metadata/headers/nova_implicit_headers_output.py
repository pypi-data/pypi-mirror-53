'''
@author: BBVA
'''

__all__ = [
    'NovaImplicitHeadersOutput'
]

class NovaImplicitHeadersOutput:

  def __init__(self):
    
    self.headersMap = {}

  def setRawHeader(self, key, valuesList):
    valuesListString = None

    if (valuesList != None):
      valuesListString = []

      for value in valuesList:
        valuesListString.append(str(value))

      # Set the Raw Header as array of str
      self.setRawHeaderInternal(key, valuesListString)
  
  def setRawHeaderInternal(self, key, valuesList):
    if valuesList != None:
      self.headersMap[key] = valuesList
  
  def getOutput(self):
    return self.headersMap