import json
import os

input_file = "contacts.json"
output_file = "contacts-sorted.json"

# Ensure file exists
if not os.path.exists(input_file):
    print(f"Error: File '{input_file}' does not exist.")
else:
    # Load the contacts and sort
    with open(input_file, "r") as file:
        contacts = json.load(file)
        
    # Sort by last_name, then by first_name
    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))
    
    # Write the sorted contacts to the new file
    with open(output_file, "w") as file:
        json.dump(sorted_contacts, file, indent=4)
        
    print(f"Sorted contacts written to '{output_file}'.")
