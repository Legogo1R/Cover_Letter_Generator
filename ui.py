import streamlit as st
from html_wrapper import wrap_job_posting

def side_bar():
    with st.sidebar: 
        model_used = st.selectbox(
        'GPT-3 Model',
        #  ('DaVinci', 'Curie', 'Babbage', 'Ada'))
        ('text-davinci-002', 'text-curie-001', 'text-babbage-001', 'text-ada-001'))
        if model_used == 'text-davinci-002': 
            st.markdown("""[Davinci](https://beta.openai.com/docs/models/davinci) is the most capable model family and can perform any task the other 
            models can perform and often with less instruction. For applications requiring a lot of 
            understanding of the content, like summarization for a specific audience and creative content
            generation, Davinci is going to produce the best results. These increased 
            capabilities require more compute resources, so Davinci costs more per API call and is not as fast as the other models.
            """)
        elif model_used == 'text-curie-001': 
            st.markdown("""[Curie](https://beta.openai.com/docs/models/curie) is extremely powerful, yet very fast. While Davinci is stronger when it 
            comes to analyzing complicated text, Curie is quite capable for many nuanced tasks like sentiment 
            classification and summarization. Curie is also quite good at answering questions and performing 
            Q&A and as a general service chatbot.
            """)
        elif model_used == 'text-babbage-001': 
            st.markdown("""[Babbage](https://beta.openai.com/docs/models/babbage) can perform straightforward tasks like simple classification. It’s also quite 
            capable when it comes to Semantic Search ranking how well documents match up with search queries.
            """)
        else: 
            st.markdown("""[Ada](https://beta.openai.com/docs/models/ada) is usually the fastest model and can perform tasks like parsing text, address 
            correction and certain kinds of classification tasks that don’t require too much nuance. 
            da’s performance can often be improved by providing more context.
            """)
        st.markdown("**Note:** Model descriptions are taken from the [OpenAI](https://beta.openai.com/docs) website")

        max_tokens = st.text_input("Maximum number of tokens:", "1949")
        st.markdown("**Important Note:** Unless the model you're using is Davinci, then please keep the total max num of tokens < 1950 to keep the model from breaking. If you're using Davinci, please keep max tokens < 3000.")

        st.subheader("Additional Toggles:")
        st.write("Only change these if you want to add specific parameter information to the model!")
        temperature = st.text_input("Temperature: ", "0.99")
        top_p = st.text_input("Top P: ", "1")
    return (model_used, int(max_tokens), float(temperature), int(top_p))

def input_data(language):
    if language == 'ru':
        st.title('Сгенерируй свое собственное сопроводительное письмо')
        info_input = st.radio('Ввод информации', ['Автоматически', 'Вручную'])
    elif language == 'en':
        st.title('Generate your own cover letter')
        info_input = st.radio('Input_data', ['Automatic', 'By hand'])
    return info_input

def auto_submit_job_form(language):
    if language == 'ru':
        tab1, tab2 = st.tabs(["Input", "Data"])
        tab1.subheader("Extract data from..")
        tab1.text_input("Job posting url")

        expander = tab1.expander("See explanation")
        expander.write('huy')

    elif language == 'en':
        tab1, tab2 = st.tabs(["Input", "Data"])

        tab1.subheader("Extract data from..")
        job_url = tab1.text_input("Job posting url:")
        job_data = wrap_job_posting(job_url)
        cv_pdf = tab1.file_uploader("Choose a CV (curriculum vitae) PDF file")
        
        # update_button = tab2.button('Update data')
        tab2.checkbox('Allow edit', key='edit_disabled')
        # if update_button:
        #     job_data = wrap_job_posting(job_url)

        with tab2.form(key='my_form_to_submit'):
            st.subheader('Job')
            company_name = st.text_input('Company Name',
                            value=job_data['vacancy-company-name'],
                            disabled=not st.session_state['edit_disabled'])
            aplying_role = st.text_input('What role are you aplying for?',
                            value=job_data['vacancy-title'],
                            disabled=not st.session_state['edit_disabled'])
            job_description = st.text_area('Job description',
                            value=job_data['vacancy-description'],
                            disabled=not st.session_state['edit_disabled'])
            st.subheader('About yourself')
            your_name = st.text_input('What is yor name?',
                            value='gf',
                            disabled=not st.session_state['edit_disabled'])
            experience_in = st.text_input('I have experience in..',
                            value='gf',
                            disabled=not st.session_state['edit_disabled'])
            excitement = st.text_input('I am excited about this job because..',
                            value='gf',
                            disabled=not st.session_state['edit_disabled'])
            passione = st.text_input('I am passionate about..',
                            value='gf',
                            disabled=not st.session_state['edit_disabled'])
            submitted = st.form_submit_button(label='Generate')

            prompt = (
                f"write my cover letter "
                f"from {your_name} "
                f"for a {aplying_role} role "
                f"at {company_name} in a conversational tone, "
                f"using the job responsibilities below as a reference "
                f"and comparing them with my resume. "
                f"Job responsibilities:{job_description}. "
                f"My resume: "
                f"I have experience in {experience_in}. "
                f"I am excited about the job because {excitement}. "
                f"I am passionate about {passione}.")
    return (submitted, prompt)

def hand_submit_job_form(language):

    if language == 'ru':
        with st.form(key='my_form_to_submit'): 
            st.subheader('Работа')
            company_name = st.text_input('Название компании')
            aplying_role = st.text_input('На какую вакансию вы подаетесь?')
            emailing_to = st.text_input('Кому адресовано это письмо?')
            st.subheader('О себе')
            your_name = st.text_input('Как вас зовут?')
            experience_in = st.text_input('У меня есть опыт в..')
            excitement = st.text_input('Я заинтересован в данной вакансии потому что..')
            passione = st.text_input('Я сильно увлечен..')
            submitted = st.form_submit_button(label='Сгенерировать')
            
            prompt = (
                f"Напиши сопроводительное письмо на работу, адресованное {emailing_to} "
                f"от имени {your_name} "
                f"на должность {aplying_role} "
                f"в компании {company_name}. " 
                f"У меня есть опыт в {experience_in}. "
                f"Я заинтересован в данной вакансии потому что  {excitement}. "
                f"Я сильно увлечен {passione}.")

    elif language == 'en':
        with st.form(key='my_form_to_submit'): 
            st.subheader('Job')
            company_name = st.text_input('Company Name')
            aplying_role = st.text_input('What role are you aplying for?')
            emailing_to = st.text_input('Who are you writing to?')
            st.subheader('About yourself')
            your_name = st.text_input('What is yor name?')
            experience_in = st.text_input('I have experience in..')
            excitement = st.text_input('I am excited about this job because..')
            passione = st.text_input('I am passionate about..')
            submitted = st.form_submit_button(label='Generate')

            prompt = (
                f"Write a cover letter to apply for a job adressed to {emailing_to} "
                f"from {your_name} "
                f"for a {aplying_role} "
                f"job at {company_name}. " 
                f"I have experience in {experience_in}. "
                f"I am excited about the job because {excitement}. "
                f"I am passionate about {passione}.")
    return (submitted, prompt)