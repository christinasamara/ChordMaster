import csv
import hashlib
import mmh3

dict1 = {"university1" : {"person1":1, "person2" : 2}, "university2" : {"person2":2, "person3" : 3}, "university3" : {"person3":3, "person4" : 4}}
dict2 = {"university2" : {"person2":2, "person3" : 3}}
dict3 = {"university3" : {"person3":3, "person4" : 4}}

for key, value in dict1.items():
    if "person1" in value.keys():
        print(value.keys())