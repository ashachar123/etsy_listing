import os
import json
from openai import OpenAI


class GptActions:
    def __init__(self):
        self.configs = self.config()
        self.client = OpenAI(api_key=self.configs.get("openai_key"))


    def send_task(self, system, prompt):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ]
        )
        if response:
            return response.choices[0].message.content

    @staticmethod
    def config():
        with open("config/Config.json", "r") as jsonobj:
            return json.load(jsonobj)

    def extract_theme(self, product):
        # Your input string

        # Splitting the string at "theme"
        parts = product.split('_Theme_')

        # Extracting the subject and themes
        subject = parts[0].replace('_', ' ')
        themes = parts[1].replace(".jpeg","").split('_') if len(parts) > 1 else []

        # Creating the dictionary
        result_dict = {"subject": subject}
        for i, theme in enumerate(themes, start=1):
            result_dict[f"theme{i}"] = theme

        return result_dict

    def create_subject(self, product):
        if ".jp" not in product:
            raw_str = self.send_task(system="you are an etsy seller",
                            prompt=f'list a subject up to 20 characters, at least two words and not using an artform, and two single worded themes from this image title: {product}, your response must be in a json format in this format: {{"subject": "", "theme1":"", "theme2":""}}' )
            print(raw_str)
            subject = json.loads("{"+raw_str+"}" if "{" not in raw_str else raw_str)

        else:
            subject = self.extract_theme(product)
        for _ in range(3):
            raw_tags = self.send_task(system="you are an etsy seo expert",
                                prompt=f"list 13 seo compatible tags up to 20 characters with spaces for etsy for {subject.get('subject')} {subject.get('theme1')} {subject.get('theme2')} vector svg clipart wall art ")
            tags = [line.split("\n")[0] for line in raw_tags[2:].split(".") if "." not in line]
            # tags = ["this is 19 charssss", "this is 18 charsss", "this is 20 charsssss", "this is 21 charsssssss", "thisiswayyyyyyymorthan20"]
            tags = [tag for tag in tags if len(tag) <=20][:13]
            if len(tags) >= 10:
                break

        return subject, tags


if __name__ == "__main__":
    GptActions().create_subject(os.listdir(f"/Users/amitshachar/Documents/etsy/31/stock")[0])