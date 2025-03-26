import re
import unicodedata
import json

def to_slug(name: str) -> str:
    # Normalize Unicode characters (e.g., é → e)
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("utf-8")
    
    # Convert to lowercase
    name = name.lower()
    
    # Replace spaces & special characters with hyphens
    name = re.sub(r'[^a-z0-9]+', '-', name)
    
    # Strip hyphens from start & end
    name = name.strip('-')
    
    return name

def append_event_type_id_to_dict(file_path, key, value):
    # Load the existing dictionary
    with open(file_path, "r") as file:
        data = json.load(file)

    # Append or modify dictionary
    if key in data:
        if isinstance(data[key], list):  # If value is a list, append
            data[key].append(value)
        else:  # Otherwise, update the value
            data[key] = value
    else:
        data[key] = value  # Add new key-value pair

    # Write the updated dictionary back to file
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
