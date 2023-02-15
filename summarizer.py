import sys
from common import inference, download, get_text_from_html, download_and_extract_text_from_pdf, tokenize_gpt2, detokenize_gpt2, split_text

MAX_TOKENS = 4000
MAX_NEW_TOKENS = 500

SUMMARY_PREPROMPT = "SUMMARIZE THE FOLLOWING DOCUMENT:\n=====\n"
SUMMARY_MIDPROMPT = ""
SUMMARY_POSTPROMPT = "\n=====\nSUMMARY:\n"

QUESTION_PREPROMPT = "ANSWER A QUESTION ABOUT THE FOLLOWING DOCUMENT:\n=====\n"
QUESTION_MIDPROMPT = "\n=====\nQUESTION: "
QUESTION_POSTPROMPT = "\nANSWER:\n"

SUMMARY_TOKEN_BUDGET = MAX_TOKENS - len(tokenize_gpt2(SUMMARY_PREPROMPT)) - len(tokenize_gpt2(SUMMARY_POSTPROMPT)) - MAX_NEW_TOKENS
QUESTION_TOKEN_BUDGET = MAX_TOKENS - len(tokenize_gpt2(QUESTION_PREPROMPT)) - len(tokenize_gpt2(QUESTION_POSTPROMPT)) - len(tokenize_gpt2(QUESTION_MIDPROMPT)) - MAX_NEW_TOKENS

def summarize(text, mode="summary", question=""):
    # Tokenize
    tokenized = tokenize_gpt2(text)

    # Split
    split = split_text(tokenized, SUMMARY_TOKEN_BUDGET if mode == "summary" else (QUESTION_TOKEN_BUDGET - len(tokenize_gpt2(question))))

    # If split has several chunks
    if len(split) > 1:
        # Summarize each chunk
        summaries = []
        for i, chunk in enumerate(split):
            # Decode the chunk
            chunk_text = detokenize_gpt2(chunk)
            # Summarize the chunk
            summaries.append(summarize(chunk_text, mode, question))

            # Print last summary and index
            print(i, summaries[-1])
            print("")

        # Join the summaries
        summaries = " ".join(summaries)
    else:
        summaries = text

    if mode == "summary":
        prompt = SUMMARY_PREPROMPT + summaries + SUMMARY_POSTPROMPT
    else:
        prompt = QUESTION_PREPROMPT + summaries + QUESTION_MIDPROMPT + question + QUESTION_POSTPROMPT
    
    return inference(prompt, MAX_NEW_TOKENS)

# print()

# Take URL from the first argument
url = sys.argv[1]

# Take the rest of the arguments and concatenate with a space
question = " ".join(sys.argv[2:]).strip()

mode = "summary" if question == "" else "question"

print("Mode:", mode)
print("Question:", question)

# If the url ends in .pdf
if url.endswith(".pdf"):
    # Get the text from the PDF
    text = download_and_extract_text_from_pdf(url)
else:
    # Download the page
    html = download(url)
    # Get the text from the URL
    text = get_text_from_html(html)

# Summarize
result = summarize(text, mode, question)

print("Final result:", result)