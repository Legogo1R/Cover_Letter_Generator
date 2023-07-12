import streamlit as st
from ui import *
import numpy as np
import openai
import os
import time
import json

# Get your GPT API key here
with open('gpt_key.txt', 'r') as txt:
    key = txt.read()
    openai.api_key = key  # API key

def generate_response(prompt, model, max_tokens, temperature, top_p):
    # response = openai.Completion.create(
    #     model=model,
    #     # messages=messages,
    #     prompt=prompt,
    #     max_tokens=max_tokens,
    #     temperature=temperature, # a number between 0 and 1 that determines how many creative risks the engine takes when generating text
    #     top_p=top_p,  # an alternative way to control the originality and creativity of the generated text.
    #     n=1, # number of predictions to generate
    #     frequency_penalty=0.3, # a number between 0 and 1. The higher this value the model will make a bigger effort in not repeating itself.
    #     presence_penalty=0.9 # a number between 0 and 1. The higher this value the model will make a bigger effort in talking about new topics.
    # )
    # return response['choices'][0]['text']
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.99,
        frequency_penalty=0.3, # a number between 0 and 1. The higher this value the model will make a bigger effort in not repeating itself.
        presence_penalty=0.9 # a number between 0 and 1. The higher this value the model will make a bigger effort in talking about new topics.
    )
    return response.choices[0].message["content"]

# Open localization json
with open('localization.json', encoding='utf-8') as localiz:
    localiz_dict = json.load(localiz)

# Create session_state variables
if 'cur_language' not in st.session_state:
    st.session_state['selectbox_label'] = 'Language'
    st.session_state['cur_language'] = 'English'
    st.session_state['languages'] = ['English', 'Russian']
    st.session_state['cur_language_short'] = 'en'
    st.session_state['edit_disabled'] = True

# Language change
if st.session_state['cur_language'] in ['English', 'Английский']:
    st.session_state['selectbox_label'] = 'Language'
    st.session_state['languages'] = ['English', 'Russian']
    st.session_state['cur_language_short'] = 'en'
elif st.session_state['cur_language'] in ['Russian', 'Русский']:
    st.session_state['selectbox_label'] = 'Язык'
    st.session_state['languages'] = ['Русский', 'Английский']
    st.session_state['cur_language_short'] = 'ru'
    
cur_lang = st.session_state['cur_language_short']  # Variable to shorten name

# Draw UI
st.selectbox(st.session_state['selectbox_label'], st.session_state['languages'], key='cur_language')
model_used, max_tokens, temperature, top_p= side_bar(cur_lang, localiz_dict)
input_info_type = input_data(cur_lang, localiz_dict)

if input_info_type in ['By hand', 'Вручную']:
    submitted, prompt = hand_submit_job_form(cur_lang, localiz_dict)
elif input_info_type in ['Automatic', 'Автоматически']:
    submitted, prompt = auto_submit_job_form(cur_lang, localiz_dict)

if submitted:
    response = generate_response(prompt,
                                 model_used,
                                 max_tokens,
                                 temperature,
                                 top_p)
    st.write(response)
