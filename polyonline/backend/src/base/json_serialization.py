import json
import importlib
from datetime import datetime, date
from base.messages import *

"""Parses a python object from a JSON string. Every Object which should be loaded needs a constuctor that doesn't need any Arguments.
Arguments: The JSON string; the module which contains the class, the parsed object is instance of."""
def json_to_class(jsonString, module = None):
    def _load(d, module):
        if isinstance(d, list):
            l = []
            for item in d:
                l.append(_load(item, module))
            return l
        elif isinstance(d, dict) and "MessageClassType" in d: #object
            t = d["MessageClassType"]
            try:
                o = eval(t+'()')
            except KeyError, e:
                raise ClassNotFoundError("Class '%s' not found in the given module!" % t)
            except TypeError, e:
                raise TypeError("Make sure there is an constuctor that doesn't take any arguments (class: %s)" % t)
            for key in d:
                if key != "MessageClassType":
                    setattr(o, key, _load(d[key], module))
            return o
        elif isinstance(d, dict): #dict
            rd = {}
            for key in d:
                rd[key] = _load(d[key], module)
            return rd
        else:
            return d
    d = json.loads(jsonString)
    if module is None:
        module = importlib.import_module('base.messages')
    return _load(d, module)

    """Dumps a python object to a JSON string. Argument: Python object"""
def class_to_json(obj):
    def _dump(obj, path):
        if isinstance(obj, (list, tuple)):
            l = []
            i = 0
            for item in obj:
                l.append(_dump(item, path + "/[" + str(i) + "]"))
                i+=1
            return l
        elif isinstance(obj, dict): #dict
            rd = {}
            for key in obj:
                rd[key] = _dump(obj[key], path + "/" + key)
            return rd
        elif isinstance(obj, str) or isinstance(obj, unicode) or isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, long) or isinstance(obj, complex) or isinstance(obj, bool) or type(obj).__name__ == "NoneType":
            return obj
        elif isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            d = {}
            d["MessageClassType"] = obj.__class__.__name__
            for key in obj.__dict__:
                d[key] = _dump(obj.__dict__[key], path + "/" + key)
            return d
    return json.dumps(_dump(obj, "/"))

class ClassNotFoundError(Exception):
    def __init__(self, msg):
        super(ClassNotFoundError, self).__init__(msg)       

if __name__ == "__main__":
    class Test1(object):
        def __init__(self):
            self.test_list = []
            for x in range(3):
                self.test_list.append(Test2())
            self.test_dict = {"2":Test3()}
            self.test_none = None

    class Test2(object):
        def __init__(self):
            self.test3 = Test3()

    class Test3(object):
        def __init__(self):
            self.test_text = 'this is a text'
            self.test_int = 1099
            self.test_bool = True
            self.test_date = datetime.now()

    t1 = Test1()
    print t1.__class__.__name__
    print t1
    j = class_to_json(t1)
    print j
    t2 = json_to_class(j, globals())
    print t2.test_dict
    t3 = [Test1(), Test2(), Test3()]
    print t3
    f = class_to_json(t3)
    print f
    g = json_to_class(f, globals())
    print g
    t4 = { 'test1': Test1(), 'test2': Test2(), 'test3': Test3() }
    k = class_to_json(t4)
    print k
    k2 = json_to_class(k, globals())
    print k2



