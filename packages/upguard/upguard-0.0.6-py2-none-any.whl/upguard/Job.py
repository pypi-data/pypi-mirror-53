import json
from .BaseObject import BaseObject
class Job(BaseObject):
  def __init__(self, appliance_url, api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, api_key, sec_key, insecure)
    self.id = None
    self.organisation_id = None
    self.source_id = None
    self.source_name = None
    self.source_type = None
    self.status = None
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['id']
    if 'organisation_id' in d:
      self.organisation_id = d['organisation_id']
    if 'source_id' in d:
      self.source_id = d['source_id']
    if 'source_name' in d:
      self.source_name = d['source_name']
    if 'source_type' in d:
      self.source_type = d['source_type']
    if 'status' in d:
      self.status = d['status']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['organisation_id'] = self.organisation_id
    d['source_id'] = self.source_id
    d['source_name'] = self.source_name
    d['source_type'] = self.source_type
    d['status'] = self.status
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
