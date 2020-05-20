# Dependencies

from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# URL of pages to be scraped

nasa_url = 'https://mars.nasa.gov/news/'
space_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
twitter_url = 'https://twitter.com/marswxreport?lang=en'
facts_url = 'https://space-facts.com/mars/'
hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


nasa_response = requests.get(nasa_url)


nasa_soup = bs(nasa_response.text, 'html.parser')


nasa_results = nasa_soup.find('div', class_="slide")


nasa_title = nasa_results.find('div', class_='content_title').find('a').text
nasa_p = nasa_results.find('div', class_='rollover_description_inner').text


featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'

browser.visit(featured_image_url)


image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(image_url)

# Go to 'FULL IMAGE'
browser.click_link_by_partial_text('FULL IMAGE')
# browser.find_link_by_partial_text('FULL IMAGE')
# time.sleep(5)

# Go to 'more info'
browser.click_link_by_partial_text('more info')
# browser.find_link_by_partial_text('more info')

# Parse HTML with Beautiful Soup
html = browser.html
image_soup = bs(html, 'html.parser')

# Scrape the URL
feat_img_url = image_soup.find('figure', class_='lede').a['href']
featured_image_url = f'https://www.jpl.nasa.gov{feat_img_url}'


tweet_response = requests.get(twitter_url)
tweet_soup = bs(tweet_response.text, 'html.parser')


tweet_results = tweet_soup.find('div', class_="js-tweet-text-container")


mars_weather = tweet_results.find('p').text


mars_facts = pd.read_html(facts_url)


mars_df = mars_facts[0]
mars_df.columns = ['Description','Value']
mars_df.set_index("Description", inplace=True)


browser.visit(hemispheres_url)


hem_response = requests.get(hemispheres_url)
hem_soup = bs(hem_response.text, 'html.parser')


itemLinks = hem_soup.find_all('div', class_='item')


site_url = 'https://astrogeology.usgs.gov'
item_urls = []


for i in itemLinks: 
    title = i.find('h3').text
    single_img = i.find('a', class_='itemLink product-item')['href']
    img_response = requests.get(site_url + single_img)
    img_soup = bs( img_response, 'html.parser')
    img_url = hemispheres_main_url + img_soup.find('img', class_='wide-image')['src']
    item_urls.append({"title" : title, "img_url" : img_url})
    

# Display list
item_urls