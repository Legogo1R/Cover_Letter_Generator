from urllib.request import urlopen
from bs4 import BeautifulSoup


tags2extract = {
    'vacancy-title': ('h1', 'data-qa'),
    'vacancy-company-name': ('span', 'class'),
    'vacancy-description': ('div', 'class'),
}

def wrap_job_posting(url):
    # url = 'https://spb.hh.ru/vacancy/81868274?from=main&hhtmFromLabel=applicant_recommended_vacancies&hhtmFrom=main'
    try:
        html_bytes  = urlopen(url).read()
        html = html_bytes.decode("utf-8")
        soup = BeautifulSoup(html, features="html.parser")

        job_data = {}
        for name, tag in tags2extract.items():
            try:
                data = soup.find(tag[0],{tag[1]:name})
                job_data[name] = data.text
            except AttributeError:  # If position is missing in url
                job_data[name] = ''
        return job_data
    
    except ValueError:  # If the url field is incorect
        job_data = {}
        for name, tag in tags2extract.items():
            job_data[name] = ''
        return job_data