import json

def get_resources_from_file(resource, filename):
    with open(filename, 'r') as f:
        metadata = json.load(f)
        if resource in metadata:
            return {resource: metadata[resource]}
        else:
            return{resource: []}