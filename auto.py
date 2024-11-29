import openai
import json

openai.api_key = '' # needed

def load_conversations(file_path):
    with open(file_path, 'r') as file:
        conversations = json.load(file)
    return conversations

def extract_messages(conversations):
    messages = []
    for convo in conversations:
        mapping = convo.get('mapping', {})
        for node_id, node in mapping.items():
            message = node.get('message')
            if not message:
                continue  # Skip if message is None
            author = message.get('author', {})
            content = message.get('content', {})
            if author.get('role') == 'user':
                parts = content.get('parts', [])
                message_text = ' '.join(part if isinstance(part, str) else str(part) for part in parts)
                messages.append(message_text)
    return messages

# Step 1: Load and process the conversations
conversations = load_conversations('conversations.json')
user_messages = extract_messages(conversations)

# Step 2: Initialize new AI instance with extracted messages
prompt = "\n".join(user_messages)

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
  ]
)

print(response['choices'][0]['message']['content'].strip())
