# TLDR (command line)

This is a command line tool that uses the openai chat api to summarize a webpage given a url.

## Setup

```bash
$ cp .env-example .env
```

Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

## Usage

```bash
$ python3 tldr.py <<URL>>
```

The code was initially written by gpt-4. I've included the code written by gpt-3.5-turbo as well for reference, but it doesn't work. The summarization itself is done by gpt-3.5-turbo.
