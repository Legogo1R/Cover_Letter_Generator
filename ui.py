import streamlit as st
from html_wrapper import wrap_job_posting

def side_bar(language, local_dict):
    with st.sidebar:
        st.subheader(local_dict['sidebar_h1'][language])
        model_used = st.selectbox(
        local_dict['gpt3_model'][language],
        #  ('DaVinci', 'Curie', 'Babbage', 'Ada'))
        ('text-davinci-003', 'gpt-3.5-turbo'))
        st.markdown(local_dict['sidebar_m1'][language])

        max_tokens = st.text_input(local_dict['max_tokens'][language], "1949")

        st.subheader(local_dict['sidebar_h2'][language])
        st.write(local_dict['sidebar_w1'][language])
        temperature = st.text_input(local_dict['temperature'][language], "0.99")
        top_p = st.text_input(local_dict['top_p'][language], "1")
    return (model_used, int(max_tokens), float(temperature), int(top_p))

def input_data(language, local_dict):
    st.title(local_dict['main_title1'][language])
    info_input = st.radio(local_dict['main_radio1_label'][language],
                          local_dict['main_radio1_choices'][language])
    return info_input

def auto_submit_job_form(language, local_dict):
    tab1, tab2 = st.tabs(local_dict['auto_job_tabs_label'][language])

    tab1.subheader(local_dict['auto_job_tab1_h1'][language])
    job_url = tab1.text_input(local_dict['job_url'][language])
    job_data = wrap_job_posting(job_url)
    cv_pdf = tab1.file_uploader(local_dict['cv_pdf'][language])
    
    update_button = tab2.button(local_dict['auto_job_tab2_b1'][language])
    tab2.checkbox(local_dict['auto_job_tab2_cb1'][language], key='edit_disabled')
    # if update_button:
    #     job_data = wrap_job_posting(job_url)

    with tab2.form(key='my_form_to_submit'):
        st.subheader(local_dict['job_form_h1'][language])
        company_name = st.text_input(local_dict['company_name'][language],
                        value=job_data['vacancy-company-name'],
                        disabled=not st.session_state['edit_disabled'])
        aplying_role = st.text_input(local_dict['aplying_role'][language],
                        value=job_data['vacancy-title'],
                        disabled=not st.session_state['edit_disabled'])
        job_description = st.text_area(local_dict['job_description'][language],
                        value=job_data['vacancy-description'],
                        disabled=not st.session_state['edit_disabled'])
        st.subheader(local_dict['job_form_h2'][language])
        your_name = st.text_input(local_dict['your_name'][language],
                        value='gf',
                        disabled=not st.session_state['edit_disabled'])
        experience_in = st.text_input(local_dict['experience_in'][language],
                        value='gf',
                        disabled=not st.session_state['edit_disabled'])
        excitement = st.text_input(local_dict['excitement'][language],
                        value='gf',
                        disabled=not st.session_state['edit_disabled'])
        passione = st.text_input(local_dict['passione'][language],
                        value='gf',
                        disabled=not st.session_state['edit_disabled'])
        submitted = st.form_submit_button(local_dict['form_submit_button'][language])

    if language == 'ru':
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
    elif language == 'en':
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

def hand_submit_job_form(language, local_dict):
    with st.form(key='my_form_to_submit'): 
        st.subheader(local_dict['job_form_h1'][language])
        company_name = st.text_input(local_dict['company_name'][language])
        aplying_role = st.text_input(local_dict['aplying_role'][language])
        emailing_to = st.text_input(local_dict['emailing_to'][language])
        st.subheader(local_dict['job_form_h2'][language])
        your_name = st.text_input(local_dict['your_name'][language])
        experience_in = st.text_input(local_dict['experience_in'][language])
        excitement = st.text_input(local_dict['excitement'][language])
        passione = st.text_input(local_dict['passione'][language])
        submitted = st.form_submit_button(local_dict['form_submit_button'][language])
        
    if language == 'ru':
        prompt = (
            f"Напиши сопроводительное письмо на работу, адресованное {emailing_to} "
            f"от имени {your_name} "
            f"на должность {aplying_role} "
            f"в компании {company_name}. " 
            f"У меня есть опыт в {experience_in}. "
            f"Я заинтересован в данной вакансии потому что  {excitement}. "
            f"Я сильно увлечен {passione}.")

    elif language == 'en':
            prompt = (
                f"Write a cover letter to apply for a job adressed to {emailing_to} "
                f"from {your_name} "
                f"for a {aplying_role} "
                f"job at {company_name}. " 
                f"I have experience in {experience_in}. "
                f"I am excited about the job because {excitement}. "
                f"I am passionate about {passione}.")
    return (submitted, prompt)