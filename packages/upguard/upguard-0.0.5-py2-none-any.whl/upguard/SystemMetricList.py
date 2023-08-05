import json
from .BaseObject import BaseObject
class SystemMetricList(BaseObject):
    
  def __init__(self, appliance_url, api_key, sec_key, insecure):
    BaseObject.__init__(self, appliance_url, api_key, sec_key, insecure)
    self.inner_list = []
  

    
  def __iter__(self):
    self.internal_iterator_counter = 0
    return self
  
  def __next__(self):
    if self.iterator_counter < self.count:
      x = self.elems[self.iterator_counter]
      self.iterator_counter += 1
      return x
    else:
      raise StopIteration
  

    
  def append(self, obj):
    self.inner_list.append(obj)
  

    
  def to_json(self):
    ll = []
    length = len(self.inner_list)
    for i in range(length):
      if i > 0:
        ll.append(",")
      ll.append(self.inner_list[i].to_json())
    return "[" + "".join(ll) + "]"
  

