import json
from jsonschema import validate

with open("synaptictrack_lattice.schema.json") as f:
    schema = json.load(f)

with open("my_lattice.json") as f:
    data = json.load(f)

validate(instance=data, schema=schema)
print("Lattice JSON is valid.")

