import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import matplotlib.pyplot as plt
import webbrowser

    
def main():
    print("This may take a few minutes!")
    
def print_all_jobs():
    print(all_jobs)


def find_ONA_jobs():
    source=urllib.request.urlopen('https://careers.journalists.org/jobs/').read()
    ONA=BeautifulSoup(source, 'html.parser')
    soup1 = ONA.find_all('div', {'class' : 'bti-ui-job-result-detail-title'})
    y=0
    titles = []
    links = []
    for x in soup1:
        yum = x.find_all('a')
        for a in yum:
            titles.append(a['title'])
            links.append("https://careers.journalists.org"+a['href'])
            y+= 1

        
    date_posted = ONA.find_all('div', {'class' : 'bti-ui-job-result-detail-age'}) 
    dates = []
    for x in date_posted:
        x = x.get_text().strip()
        dates.append(x)
    
    organization = ONA.find_all('div', {'class' : 'bti-ui-job-result-detail-employer'}) 
    organizations = []
    for x in organization:
        x = x.get_text().strip()
        organizations.append(x)
    
    location = ONA.find_all('div', {'class' : 'bti-ui-job-result-detail-location'}) 
    locations = []
    for x in location:
        x = x.get_text().strip()
        locations.append(x)
    
    
    ONA_jobs = pd.DataFrame({'Job Title': titles, 'Organization': organizations, 'Link' : links, 'Date Posted': dates, 'Location' : locations})
    
    return ONA_jobs

ONA_jobs = find_ONA_jobs()

def find_JJ_jobs():

    source3=urllib.request.urlopen('http://www.journalismjobs.com/job-listings?keywords=&location=').read()
    JJ=BeautifulSoup(source3, 'html.parser')

    soup3 = JJ.find_all('div', {'class' : 'result'})
    soup4 = JJ.find_all('div', {'class' : 'title'})
    y=0
    titles3 = []
    links3 = []
    for t in soup3:
        for x in soup4: 
            z = x.get_text().strip()
            titles3.append(z)
            yum3 = x.find_all('a')
            for a in yum3:
                links3.append("http://www.journalismjobs.com"+a['href'])
                y+= 1
 
    date_posted3 = JJ.find_all('li', {'class' : 'posted'})
    dates3 = []
    for t in soup3:
        for x in date_posted3:
            x = x.get_text().strip()
            dates3.append(x)
    
    organization3 = JJ.find_all('div', {'class' : 'company'}) 
    organizations3 = []
    for t in soup3:
        for x in organization3:
            x = x.get_text().strip()
            organizations3.append(x)

    location3 = JJ.find_all('li', {'class' : 'location'}) 
    locations3 = []
    for t in soup3:
        for x in location3:
            x = x.get_text().strip()
            locations3.append(x)  
        
    JJ_jobs = pd.DataFrame({'Job Title': titles3, 'Organization': organizations3, 'Link' : links3, 'Date Posted': dates3, 'Location' : locations3})
    JJ_jobs = JJ_jobs.drop_duplicates()
    return JJ_jobs

JJ_jobs = find_JJ_jobs()

def find_IRE_jobs():

    source2=urllib.request.urlopen('https://www.ire.org/jobs/type/job-posting/').read()
    IRE=BeautifulSoup(source2, 'html.parser')


    soup2 = IRE.find_all('td', {'class' : 'title3'})
    y2=0
    links2 = []
    for x in soup2:
        yum2 = x.find_all('a')
        for a in yum2:
            links2.append("https://www.ire.org"+a['href'])
            y2+= 1

    IRE_jobs = pd.read_html("https://www.ire.org/jobs/type/job-posting/", header=None)[0]
    IRE_jobs.columns = ["Job Title", "Organization", "Location", "Date Posted"]

    links2 = pd.Series(links2)

    IRE_jobs['Link'] = links2.values
    
    return IRE_jobs

IRE_jobs = find_IRE_jobs()

def find_all_jobs():

    job_sources = [ONA_jobs, IRE_jobs, JJ_jobs]

    all_jobs = pd.concat(job_sources)

    all_jobs['City'], all_jobs['State'] = all_jobs['Location'].str.split(', ', 1).str
    
    state_abvns = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
        }

    all_jobs.State = all_jobs.State.replace(state_abvns, regex=True) 
    
    all_jobs = all_jobs.drop('Location', axis=1)

    return all_jobs


all_jobs = find_all_jobs()

def where_are_jobs():
    
    job_locations = all_jobs.groupby('State').count()
    job_locations = job_locations.sort_values('Job Title', ascending=False)

    ax = job_locations['Job Title'].plot(kind='bar', title ="Journalism Jobs by State", figsize=(15, 5), legend=False, fontsize=12)
    ax.set_xlabel("State", fontsize=12)
    ax.set_ylabel("Number of Jobs", fontsize=12)
    plt.show()
    
def jobs_in():
    State = str(input('Enter state:'))
    all_jobs['State'].fillna(value=0).astype(str)
    print  (all_jobs.loc[all_jobs['State'].str.contains(State, na=False, case=False)])

def search_jobtitles():
    keyword = str(input('Enter keyword:'))
    all_jobs['Job Title'].fillna(value=0).astype(str)
    print  (all_jobs.loc[all_jobs['Job Title'].str.contains(keyword, na=False, case=False)])

def see_job_site():
    organization = str(input('Enter organization to see jobs on their website:'))
    all_jobs['Organization'].fillna(value=0).astype(str)
    listed = all_jobs.loc[all_jobs['Organization'].str.contains(organization, na=False, case=False)]
    for row in listed.Link:
        row = row.strip()
        webbrowser.open_new_tab(row)
        
main()
print("----All jobs!----")
print_all_jobs()
print("----Find a job by location (example: Illinois----")
jobs_in()
print("----Find a job by keyword (example: editor)----")
search_jobtitles()
print("----Open webpages from an organization's postings (example: NPR)----")
see_job_site()
print("----Where the jobs are: see graph!----")
where_are_jobs()
