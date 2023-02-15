# Summarizer

This repository contains the code from this video:

[Build a Summarizer and Q&A with ChatGPT/GPT-3 APIs - Point AI series](https://youtu.be/OgSpLwTVyHQ)

# Install

```
git clone https://github.com/sergevar/summarizer.git
cd summarizer
pip install -r requirements.txt
cp .env.example .env
```

# Add your API key

https://platform.openai.com/account/api-keys

Set in `.env` file:

`OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxx"`

# Run

## Summary mode

```
python3 summarize.py https://URLofWebPageOrPDFToSummarize
```

## Q&A mode

```
python3 summarize.py https://URLofWebPageOrPDFToSummarize "Your question here"
```
