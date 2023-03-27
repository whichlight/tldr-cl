import sys
import openai
import os
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import time
import math

load_dotenv()

# Set up API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_webpage(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def extract_main_text(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove irrelevant elements
    for element in soup.find_all(['header', 'footer', 'nav', 'aside']):
        element.decompose()

    text = soup.get_text(separator=" ")
    return text


def split_text(text, max_tokens=3000):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)

        if len(" ".join(current_chunk)) >= max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def summarize(text):
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following text for me: {text}"},
        ],
    )
    summary = result.choices[0].message.content
    return summary

def get_elapsed_time(initial_time):
    return math.floor((time.time() - initial_time))


def main():
    start = time.time()
    
    if len(sys.argv) < 2:
        print("Usage: python summarize.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    try:
        html = fetch_webpage(url)
        main_text = extract_main_text(html)
        text_chunks = split_text(main_text, 3000)

        summaries = []

        print(f"Number of words: {len(main_text.split())}\n")

        for count, chunk in enumerate(text_chunks):
            s = summarize(chunk)
            print(f"***** summarized chunk {count+1} of {len(text_chunks)} at {get_elapsed_time(start)}s")
            print(s + "\n")
            summaries.append(s)

        final_summary = summarize(' '.join(summaries))

        print(f"***** Cumulative summary for {url} at {get_elapsed_time(start)}s:")
        print(final_summary)
    
    except Exception as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    main()