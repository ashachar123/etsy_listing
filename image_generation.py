from openai import OpenAI
import requests
from PIL import Image
from datetime import datetime

client = OpenAI(api_key="")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "I need 4 specific design illustration ideas and settings to sell on Etsy such as skeleton ballerinas in a gothic artstyle, each idea has to have one subject that is the main focus."},
    ]
)

# Extracting and displaying the ideas
if response:
    message = response.choices[0].message.content
    lines = message.split('\n')
    ideas = []

    for line in lines:
        if line.strip():
            # Assuming each line is an idea and using the first sentence as the nam
            try:
                num = int(line[0])
                line = line[2:]

                ideas.append(line)

            except:
                pass




    print(ideas)
else:
    print("No response received.")

"""create a simple thick lined monoline vector Illiustration of unicorns in knight armor with a Gothic design, blending mythological creatures with medieval themes
 make it using only one shade of black with bold clear lines on a plain white background and use a somewhat simple design"""
for index, design in enumerate(ideas):
    for num in [1,2,3,4]:
        image = client.images.generate(
          model="dall-e-3",
          prompt=f"""create a very simple bold lined thick lined monoline vector Illiustration of {design}, use minimal lines and
         make it using only one shade of black with bold clear lines on a plain white background and use a somewhat simple design""",
          n=1,
          size="1024x1024"
        )
        url = image.data[0].url
        # response = requests.get(url)
        img = Image.open(requests.get(url, stream=True).raw)
        img.save(f"/Users/amitshachar/Downloads/DALL{index}_{num}_{str(datetime.now()).replace(':', '.').replace(' ', '')}.png")
