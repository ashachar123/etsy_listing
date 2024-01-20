import os
import re
import json
from openai import OpenAI
import requests
from PIL import Image
from datetime import datetime

client = OpenAI(api_key="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")
product = os.listdir("/Users/amitshachar/Documents/etsy/31/Stock")[0]


def send_task(system, prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ]
    )

    # Extracting and displaying the ideas
    if response:
        return response.choices[0].message.content


def create_dict(input_string):

    # Extract the subject
    subject_start = input_string.find('Subject: "') + len('Subject: "')
    subject_end = input_string.find('"\n\nThemes:', subject_start)
    subject = input_string[subject_start:subject_end]

    # Extract the themes
    themes_start = input_string.find('Themes: \n') + len('Themes: \n')
    themes_str = input_string[themes_start:]
    themes_list = themes_str.split('\n')

    # Create the dictionary
    result_dict = {"subject": subject}
    for i, theme in enumerate(themes_list, start=1):
        theme = theme.split('. ')[1] if '. ' in theme else theme
        result_dict[f"theme{i}"] = theme

    print(result_dict)


product = os.listdir("/Users/amitshachar/Documents/etsy/32/Stock")[0]
for _ in (1,2,3,4,5,5,5,5,5,5,5):
    raw_str = send_task(system="you are an etsy seller", prompt=f"list a subject up to 20 characters, at least two words and not using an artform,  and two single worded themes from this image title: {product}, your response muust be in a json format in this format: {{subject:'' , theme1:'', theme2:''}}",)
    raw_str = "{"+raw_str+"}" if "{" not in raw_str else raw_str
    print(raw_str)
    print(json.loads(raw_str))