import json
import openai

# Load raw leads data
with open('leads.json', 'r') as f:
    leads = json.load(f)

# Dummy ranking: sort by name length (replace with GPT-4 API call if desired)
ranked_leads = sorted(leads, key=lambda x: len(x.get('name', '')), reverse=True)

with open('filtered_leads.json', 'w') as f:
    json.dump(ranked_leads, f, indent=4)

print("Leads filtered and saved to filtered_leads.json")
