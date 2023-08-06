import json
from .BaseObject import BaseObject
class Policy(BaseObject):
  def __init__(self, appliance_url, api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, api_key, sec_key, insecure)
    self.id = None
    self.name = None
  def from_dict(self, d):
    if 'id' in d:
      self.id = d['id']
    if 'name' in d:
      self.name = d['name']
  def to_dict(self):
    d = {}
    d['id'] = self.id
    d['name'] = self.name
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def load(self):
    obj = self.http_get("/api/v2/policies/" + str(self.id) + ".json")
    from_hash(obj)
  

    
  def save(self):
    if self.id == 0 or self.id == None:
      return self.create()
    else:
      return self.update()
  

    
  def create(self):
    d = self.to_dict()
    out = self.http_post("/api/v2/policies.json", d)
    self.from_dict(out)
  

    
  def update(self):
    d = self.to_dict()
    self.http_put("/api/v2/policies/" + str(self.id) + ".json", d)
  

    
  def delete(self):
    self.http_delete("/api/v2/policies/" + str(self.id) + ".json")
  

