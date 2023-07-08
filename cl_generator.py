import streamlit as st
import numpy as np
import pandas as pd
import openai
import os
import time

openai.api_key = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

st.title('Generate your own cover letter')

with st.form(key='my_form_to_submit'): 
    st.subheader('Job')
    company_name = st.text_input('Company Name')
    aplying_role = st.text_input('What role are you aplying for?')
    emailing_to = st.text_input('Who are you writing to?')
    st.subheader('Yourself')
    your_name = st.text_input('What is yor name?')
    experience_in = st.text_input('I have experience in..')
    excitement = st.text_input('I am excited about this job because..')
    passione = st.text_input('I am passionate about..')
    submitted = st.form_submit_button(label='Submit')

    prompt = (
        f"Write a cover letter to {emailing_to} "
        f"from {your_name} "
        f"for a {aplying_role} "
        f"job at {company_name}. " 
        f"I have experience in {experience_in}. "
        f"I am excited about the job because {excitement}. "
        f"I am passionate about {passione}."
    )

    if submitted:
        response = get_completion(prompt)
        st.write(response)
