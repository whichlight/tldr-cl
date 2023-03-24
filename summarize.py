import sys
import openai
import os
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

load_dotenv()


# Set up API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_webpage(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")
    return text


'''
models are gpt-3.5-turbo and gpt-4
'''

def summarize(text):
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize this text for me: {text}"},
        ],
    )
    summary = result.choices[0].message.content
    return summary


def main():
    if len(sys.argv) < 2:
        print("Usage: python summarize.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    try:
        html = fetch_webpage(url)
        text = extract_text(html)
        summary = summarize(text)

        print(f"Summary for {url}:")
        print(summary)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()