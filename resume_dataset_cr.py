from urllib.request import urlopen
from utils import get_dir_of_obj
from bs4 import BeautifulSoup
from googletrans import Translator
import os
import json
from collections import defaultdict


tags2extract = [
    'name',
    'email',
    'random_info',
    'workexperience',
    'education',
    'skills'
]

html_folder = 'resume_dataset/html/'

text_classif_data = defaultdict(dict)
counter = 0
for filename in os.listdir(html_folder):

    with open(f'{html_folder}{filename}', 'r') as resume:
        html = resume.read()

    soup = BeautifulSoup(html, features="html.parser")

    for name in tags2extract:
        data = soup.find(class_=name)
        if name == 'workexperience':

            i = 0
            text2append = ''
            for child in data.children:
                if len(child.get_text(strip=True)) != 0:
                    text2append += child.text + '. '
                    i += 1
                    if i == 2:
                        stripped_text = text2append.replace("\n", " ").strip()
                        encoded_string = stripped_text.encode("ascii", "ignore")  # Remove non ASCII symbols
                        decode_string = encoded_string.decode()
                        text_classif_data[counter] = {'text': decode_string,
                                        'class': name}
                        counter += 1
                        i = 0
                        text2append = ''

        else:
            stripped_text = data.text.replace("\n", " ").strip()
            encoded_string = stripped_text.encode("ascii", "ignore")  # Remove non ASCII symbols
            decode_string = encoded_string.decode()
            if name == 'email':
                decode_string = decode_string.replace(" ", "")
            text_classif_data[counter] = {'text': decode_string,
                                        'class': name}
            counter += 1

json_filename = 'text_classif_en.json'
json_folder = 'resume_dataset/json/'
with open(f'{json_folder}{json_filename}', 'w+', encoding='utf-8') as txt:
        json.dump(text_classif_data, txt, ensure_ascii=False, indent=4)


# Translate to Rus
translator = Translator()
for id, example in text_classif_data.items():
    for label, text in example.items():
        if label =='email':
                example[label] = text
        else: 
            translated = translator.translate(dest='ru', text=text)
            example[label] = translated.text

json_filename = 'text_classif_ru.json'
json_folder = 'resume_dataset/json/'
with open(f'{json_folder}{json_filename}', 'w+', encoding='utf-8') as txt:
        json.dump(text_classif_data, txt, ensure_ascii=False, indent=4)

