import json
import collections

class User:
    def __init__(self):
        self.group = None
        self.subgroup = 0
        self.request = "False"
        self.request_day = None
        self.request_week = None
        self.request_group = None
        self.request_subgroup = 0

class JSONUserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            Dict={}
            Dict['group'] = obj.group 
            Dict['subgroup'] = obj.subgroup 
            Dict['request'] = obj.request
            Dict['request_day'] = obj.request_day
            Dict['request_week'] = obj.request_week
            Dict['request_group'] = obj.request_group 
            Dict['request_subgroup'] = obj.request_subgroup 

            return dict(_User_object=Dict)
        else:
            return json.JSONEncoder.default(self, obj)

def json_as_python_User(dct):
    if '_User_object' in dct:
        obj = User()
        Dict = dct['_User_object']
        obj.group = Dict['group'] 
        obj.subgroup = int(Dict['subgroup'])
        obj.request = Dict['request']
        obj.request_day = Dict['request_day']
        obj.request_week = Dict['request_week']
        obj.request_group  = Dict['request_group'] 
        obj.request_subgroup = int(Dict['request_subgroup'])
        return obj
    return dct

class JSONSetEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, collections.Set):
            return dict(_set_object=list(obj))
        else:
            return json.JSONEncoder.default(self, obj)


def json_as_python_set(dct):
    if '_set_object' in dct:
        return set(dct['_set_object'])
    return dct