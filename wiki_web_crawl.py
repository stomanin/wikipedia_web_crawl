"""
 == Wikipedia web crawl ==

 $ python3 wiki_web_crawl.py 'https://en.wikipedia.org/wiki/Cat' 'https://en.wikipedia.org/wiki/Philosophy'

"""

from sys import argv
import requests
from time import sleep
from bs4 import BeautifulSoup

starting_page = argv[1]
target_url = argv[2]
#starting_page = 'https://en.wikipedia.org/wiki/Cat'
#target_url='https://en.wikipedia.org/wiki/Philosophy'


def continue_crawl(search_history, target_url, max_steps=25):
	"""
	This function gets in input:
	- search_history: list of URLs to wiki articles (strings)
	- target_url: url of the last page of the crawl
	returns False when we crawl to the target_url or we enter an infinite crawling loop, otherwise returns True
	"""
	if search_history[-1] == target_url:
		print('Target URL found!')
		return False
	elif len(search_history) > max_steps:
		print('More than 25 tentatives, this is taking too long')
		return False
	elif search_history[-1] in search_history[:-1]:
		print('Looks like we got into a loop')
		return False
	else:
		return True

def parse_to_first_anchor(page_url, p_limit=5, wiki_link_start='/wiki/'):
	"""
	This function parses the HTML of the Wikipedia page given in input, 
	and returns a string of the first anchor link to another Wikipedia page
	"""
	# get the HTML of the page
	response = requests.get(page_url)
	page_html = response.text
	#print(page_html[:100])
	# use BeautifulSoup for parsing
	htmlsoup = BeautifulSoup(page_html, 'html.parser')

	#print(htmlsoup.prettify())

	# HTML structure of a Wikipedia page to get to the first paragraph of text for an article:
	# <body>
	#  <div id="bodyContent">
	#   <div id="mw-content-text">
	#    <div class="mw-parser-output">
	#     <p>
	#      <a>

	#find the first <div> with class="mw-parser-output"
	first_div = htmlsoup.find(id="mw-content-text").find(class_="mw-parser-output")

	#loop over all paragraphs and anchors to find first applicable anchor link
	for p in first_div.find_all('p', recursive=False, limit=p_limit):
		for a in p.find_all('a', recursive=False):
			if a.get('href').startswith(wiki_link_start):
				return 'https://en.wikipedia.org' + a.get('href')
				break


search_history = [starting_page]

while continue_crawl(search_history,target_url):
	# parse html of last visited page to get first link to next Wiki article  
	linkfound = parse_to_first_anchor(search_history[-1])
	# if found, append it to search history
	if linkfound:
		print(linkfound)
		search_history.append(linkfound)
	else:
		print("No links here!")
		break

	# sleep for a second to avoid overloading Wikipedia with get requests
	sleep(1)


#print(search_history)
