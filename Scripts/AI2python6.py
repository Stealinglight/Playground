#   ___     _____       ____    _   ______           __            _____        __   
#  / _ |___/ / _ \__ __/ __/___(_) / __/ /____ _____/ /____ ____  / ___/__  ___/ /__ 
# / __ / _  / ___/ // / _// __/ / _\ \/ __/ _ `/ __/ __/ -_) __/ / /__/ _ \/ _  / -_)
#/_/ |_\_,_/_/   \_, /_/ /_/ /_/ /___/\__/\_,_/_/  \__/\__/_/    \___/\___/\_,_/\__/ 
#               /___/                             
### LESSON 6 - Web Scraping and API calls ###

import requests
import bs4
import itertools

""" #this is a static site that has the full text to Romeo and Juliet
WEBSITE = "C:/Users/ndeguz/Downloads/NickiDeGuzman"

#use the requests module to get the site
get_site = requests.get(WEBSITE)

#this will throw an error if something happens to the site. Otherwise, it will return None
get_site.raise_for_status()

#print out the full text found on the website
print(get_site.text)

#turn the content of the site into an iterator
loop_over_lines = get_site.iter_lines()

#utilize itertools to just get the first 10 lines of the site content
for line in itertools.islice(loop_over_lines, 10):
    print(line) """

#prints out the website as bytes only
#print(get_site.content)

###############
### TO DO - try out the above code block with websites of your choosing. See what output they provide!
###############

###############
### Why You Should NOT Use RegEx to Parse HTML https://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags/1732454#1732454
###############

###############
### A free online API for you to test things with fake data https://jsonplaceholder.typicode.com/
###############

###############
### Beautiful Soup Exercise
###############
### Use Shift+Alt+A (Windows) or Shift+Option+A (Mac) to uncomment the block below

# This code is used to scrape a website of job postings and return the job title, company, and location if the word "Python" is in the job title. 
# The code is run as a function called "scrape_jobs" that takes the website as an argument. The function uses the requests module to make a GET request to the website and then uses BeautifulSoup to parse the HTML.
# The function returns a list of dictionaries, where each dictionary contains the job title, company, and location for each job posting.

SOUP_WEBSITE = "https://realpython.github.io/fake-jobs/"

###TO DO - make a request here for BS4 to use
res = requests.get(SOUP_WEBSITE)

soup_it = bs4.BeautifulSoup(res.content, "html.parser")

results = soup_it.find_all('div', class_='card-content')
for result in results:
    title = result.find('h2', class_='title is-5').text
    company = result.find('h3', class_='subtitle is-6 company').text
    location = result.find('p', class_='location').text
    if 'python' in title.lower(): 
        print(f"{title} | {company} | {location}")

