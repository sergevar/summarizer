import chardet
import openai
import os

import dotenv
dotenv.load_dotenv()
# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

# Use GPT2TokenizerFast to tokenize the text
def tokenize_gpt2(text):
    from transformers import GPT2TokenizerFast

    # Suppress warning: Token indices sequence length is longer than the specified maximum sequence length for this model (3874 > 1024). Running this sequence through the model will result in indexing errors
    import logging
    logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)

    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    return tokenizer.encode(text)

def detokenize_gpt2(text):
    from transformers import GPT2TokenizerFast

    # Suppress warning: Token indices sequence length is longer than the specified maximum sequence length for this model (3874 > 1024). Running this sequence through the model will result in indexing errors
    import logging
    logging.getLogger("transformers.tokenization_utils_base").setLevel(logging.ERROR)           

    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    return tokenizer.decode(text)

def openai_inference_gpt3(prompt, max_new_tokens):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=max_new_tokens
    )
    return response.choices[0].text

def inference(prompt, max_new_tokens):
    result = openai_inference_gpt3(prompt, max_new_tokens)

    # Log the prompt into history.txt
    with open("gpt_history.txt", "a") as f:
        # Write the prompt, the separator "<|>" and the completion result
        f.write(prompt + "<|>" + result + "\n\n\n-----------\n\n\n")
        
    return result
    
# Download the URL pretending to be a Firefox browser
def download(url):
    import requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
    }
    return requests.get(url, headers=headers)

def get_text_from_html(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup.get_text()
import chardet

def download_and_extract_text_from_pdf(url):
    # Download the PDF
    pdf = download(url).content

    # Extract the text from the PDF
    text = extract_text_from_pdf(pdf)

    return text

def extract_text_from_pdf(pdf):
    # Extract the text from the PDF
    import io
    from pdfminer.high_level import extract_text_to_fp
    from pdfminer.layout import LAParams

    # Create a buffer
    buf = io.StringIO()

    # Extract the text from the PDF
    extract_text_to_fp(io.BytesIO(pdf), buf, laparams=LAParams())

    # Get the text
    text = buf.getvalue()

    # Close the buffer
    buf.close()

    return text

def split_text(tokenized, budget):
    # Split the text into 4000 tokens chunks
    split = []
    for i in range(0, len(tokenized), budget):
        split.append(tokenized[i:i+budget])

    # If the last chunk is smaller than budget, pad it from the previous chunk up to budget
    if len(split[-1]) < budget and len(split) > 1:
        # Calculate the remaining budget
        remaining_budget = budget - len(split[-1])
        # Pad the last chunk with the remaining budget
        split[-1] = split[-2][-remaining_budget:] + split[-1]

    return split
