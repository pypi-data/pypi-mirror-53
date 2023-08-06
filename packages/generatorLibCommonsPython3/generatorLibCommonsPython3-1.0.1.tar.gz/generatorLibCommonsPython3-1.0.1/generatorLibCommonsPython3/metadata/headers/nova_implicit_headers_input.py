'''
@author: BBVA
'''

__all__ = [
    'NovaImplicitHeadersInput'
]

import re

class NovaImplicitHeadersInput:

  def __init__(self, headersMap):
    
    self.headersMap = headersMap

  def getRawHeaderBoolean(self, key):
    outcome = None

    # Get the RAW Header as Array
    valuesListString = self.getRawHeader(key)

    if valuesListString != None:
      outcome = []

      for valueString in valuesListString:
          
        # Remove all blanks
        valueString = re.sub(r"\s+", "", valueString)
        
        # Create the boolean
        valueString = valueString != None and valueString == "true"
        
        # Append to the array
        outcome.append(valueString)

    return outcome

  def getRawHeaderFloat(self, key):
    outcome = None

    # Get the RAW Header as Array
    valuesListString = self.getRawHeader(key)

    if valuesListString != None:
      outcome = []

      for valueString in valuesListString:
        outcome.append(float(valueString))

    return outcome

  def getRawHeaderInt(self, key):
    outcome = None

    # Get the RAW Header as Array
    valuesListString = self.getRawHeader(key)

    if valuesListString != None:
      outcome = []

      for valueString in valuesListString:
        outcome.append(int(valueString))

    return outcome
  
  def getRawHeaderString(self, key):
    return self.getRawHeader(key)

  def getRawHeader(self, key):
    valuesListString = None
  
    if self.headersMap is not None:
      valuesListString = self.getRawHeaderInternal(key)
  
    return valuesListString

  def getRawHeaderInternal(self, key):
    outcome = None
    
    if self.headersMap.has_key(key):

      outcome = self.headersMap.get(key).split(",")
      
    return outcome