import json
from .BaseObject import BaseObject
class Environment(BaseObject):
  def __init__(self, appliance_url, api_key, sec_key, insecure = False):
    BaseObject.__init__(self, appliance_url, api_key, sec_key, insecure)
    self.description = None
    self.id = None
    self.name = None
    self.node_rules = None
    self.short_description = None
  def from_dict(self, d):
    if 'description' in d:
      self.description = d['description']
    if 'id' in d:
      self.id = d['id']
    if 'name' in d:
      self.name = d['name']
    if 'node_rules' in d:
      self.node_rules = d['node_rules']
    if 'short_description' in d:
      self.short_description = d['short_description']
  def to_dict(self):
    d = {}
    d['description'] = self.description
    d['id'] = self.id
    d['name'] = self.name
    d['node_rules'] = self.node_rules
    d['short_description'] = self.short_description
    return d
  def to_json(self):
    d = self.to_dict()
    return json.dumps(d)
    
  def load(self):
    obj = self.http_get("/api/v2/environments/{id}.json")
    from_hash(obj)
  

    
  def save(self):
    if self.id == 0 or self.id == None:
      return self.create()
    else:
      return self.update()
  

    
  def create(self):
    d = self.to_dict()
    out = self.http_post("/api/v2/environments.json", d)
    self.from_dict(out)
  

    
  def update(self):
    d = self.to_dict()
    del d["id"]
    del d["organisation_id"]
    self.http_put("/api/v2/environments/{id}.json", d)
  

    
  def delete(self):
    self.http_delete("/api/v2/environments/{id}.json")
  

    
  def nodes(self):
    obj = self.http_get("/api/v2/environments/{id}/nodes.json")
    the_list = NodeList(self.appliance_url, self.api_key, self.sec_key, self.insecure)
    for x in obj:
      elem = Node(self.appliance_url, self.api_key, self.sec_key, self.insecure)
      if "id" in x:
        elem.id = x["id"]
      if "name" in x:
        elem.name = x["name"]
      the_list.append(elem)
    return the_list
  

