import openai
import json

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

openai.api_key = config.get('openai_api_key')

def generate_followup(email_context):
    prompt = f"Generate a friendly follow-up email for this context: {email_context}"
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response['choices'][0]['message']['content']

if __name__ == '__main__':
    email_context = "No response from previous email outreach. Follow-up politely."
    followup_email = generate_followup(email_context)
    print("Generated Follow-Up Email:")
    print(followup_email)
