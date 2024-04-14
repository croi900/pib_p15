import json
import requests


def auto_correct ():
    headers = {"Authorization": "API_KEY"}

    url = "https://api.edenai.run/v2/text/chat"
    with open("output.txt", "r") as file:
        corrected_text = file.read()

    payload = {
        "providers": "openai",
        "text": corrected_text,
        "chatbot_global_action": "Can you rewrite this text into a correct one? OCR was used and this is the generated text. "
                                 "It is not entirely accurate, as some words might be misspelled. "
                                 "The original meaning and format of the text must not be changed.",
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 150,
        "fallback_providers": ""
    }

    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)

    with open("output.txt", "w") as output_file:
        output_file.write(result['openai']['generated_text'])
