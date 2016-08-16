import json


class User:
    def __init__(self):
        self.group = None
        self.subgroup = None
        self.request_day = None
        self.request_week = None
        self.request_group = None
        self.request_subgroup = None

class JSONUserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            Dict={}
            Dict['group'] = obj.group 
            Dict['subgroup'] = obj.subgroup 
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
        obj.subgroup = Dict['subgroup']
        obj.request_day = Dict['request_day']
        obj.request_week = Dict['request_week']
        obj.request_group  = Dict['request_group'] 
        obj.request_subgroup = Dict['request_subgroup']
        return obj
    return dct

