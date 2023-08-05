import json
from .BaseObject import BaseObject
class ConnectionManagerGroup(BaseObject):
  def __init__(self, appliance_url, api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, api_key, sec_key, insecure)
    self.id = None
    self.name = None
    self.organisation_id = None
    self.status = None
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['id']
    if 'name' in d:
      self.name = d['name']
    if 'organisation_id' in d:
      self.organisation_id = d['organisation_id']
    if 'status' in d:
      self.status = d['status']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    d['organisation_id'] = self.organisation_id
    d['status'] = self.status
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def connection_managers(self):
    obj = self.http_get("todo")
    the_list = ConnectionManagerList(self.appliance_url, self.api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = ConnectionManager(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      the_list.append(elem)
    return the_list
  

