import sys 
import json
import yaml

path = sys.argv[1]
try:
    with open(path) as f:
        data = yaml.safe_load(f)
    print("VALID\n")
    print(json.dumps(data, indent=2, default=str))
except yaml.YAMLError as e:
    print("INVALID")
    print(e)