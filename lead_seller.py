import json

with open('filtered_leads.json', 'r') as f:
    leads = json.load(f)

# Package leads into chunks of 10
packages = [leads[i:i+10] for i in range(0, len(leads), 10)]

with open('lead_packages.json', 'w') as f:
    json.dump(packages, f, indent=4)

print("Lead packages created in lead_packages.json")
