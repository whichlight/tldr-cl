import openai
from bs4 import BeautifulSoup
import requests

# Set up API key
openai.api_key = "YOUR_API_KEY_HERE"

# Input URL
url = input("Enter the URL: ")

# Extract text from URL
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
text = soup.get_text()

# Prepare messages for chat API
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"Can you please summarize the web page at {url} ?"},
    {"role": "assistant", "content": text},
]

# Use chat API to summarize text
response = openai.Completion.create(
    engine="davinci",
    prompt=messages,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5
)

# Extract summary from response
summary = response.choices[0].text

# Output summary to command line
print(summary)