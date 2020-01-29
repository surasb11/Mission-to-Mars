# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests
import time
import re

# MAC - Set browser
def init_browser():
	
	executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
	return Browser("chrome", **executable_path, headless=False)
	
mars_info = {}
	
# Mars News
def scrape_info():
	
	browser = init_browser()
	
	# Visit Nasa news url
	url_news = "https://mars.nasa.gov/news/"
	browser.visit(url_news)
		
	# HTML Object
	html_news = browser.html
	soup = BeautifulSoup(html_news, "html.parser")
		
	# Scrape the latest News Title and Paragraph Text
	news_title = soup.find("div", class_ = "content_title").text
	news_paragraph = soup.find("div", class_ = "article_teaser_body").text
	
	mars_info["news_title"] = news_title
	mars_info["news_paragraph"] = news_paragraph 


# Featured Image
	
	# Visit JPL Featured Space Image url
	url_spaceimage = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url_spaceimage)
	
	# HTML Object
	img_html = browser.html
	img_soup = BeautifulSoup(img_html, "html.parser")

	# Find image url to the full size
	featured_image = img_soup.find("article")["style"].replace('background-image: url(','').replace(');', '')[1:-1]
	
	# Display url
	main_url = "https://www.jpl.nasa.gov"
	
	# Connect website url with scrapped route
	featured_image_url = main_url + featured_image


	mars_info["featured_image_url"] = featured_image_url
	
	
# Mars Weather
	
	# Visit Mars Weather twitter url
	url_weather = "https://twitter.com/marswxreport?lang=en"
	browser.visit(url_weather)
	
	# HTML Object
	weather_html = browser.html
	weather_soup = BeautifulSoup(weather_html, "html.parser")
	
	# Scrape the latest Mars weather tweet from the page
	weather = weather_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
	
	# Remove the anchor from paragraph
	weather.a.decompose()
	weather = weather.text
	
	# Clean up the text
	mars_weather = weather.replace(" \n", '')
	
	mars_info["mars_weather"] = mars_weather
	

# Mars Facts

	# Visit the Mars Facts webpage and use Pandas to scrape the table
	url_facts = "https://space-facts.com/mars/"

	# Use Pandas - read_html - to scrape tabular data from a page
	mars_facts = pd.read_html(url_facts)
	
	# Find the mars facts DataFrame in the list
	mars_df = mars_facts[0]

	# Create Data Frame
	mars_df.columns = ["Description", "Value"]

	# Set index to Description
	mars_df.set_index("Description", inplace=True)

	# Save html code to folder Assets
	html_table = mars_df.to_html()

	# Strip unwanted newlines to clean up the table
	html_table.replace("\n", '')

	# Save html code
	mars_df.to_html("mars_facts_data.html")
	
	mars_info["mars_facts"] = html_table


# Mars Hemispheres
	
	# Visit the USGS Astrogeology Science Center url
	url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(url_hemisphere)
	
	# HTML Object
	html_hemisphere = browser.html
	hem_soup = BeautifulSoup(html_hemisphere, "html.parser")
	
	# Find containers whcih has mars hemispheres information
	hemispheres = hem_soup.find_all("div", class_="item")

	# Create empty list
	hemispheres_info = []

	# Sign main url for loop
	hemispheres_url = "https://astrogeology.usgs.gov"

	# Loop through the list of all hemispheres information
	for i in hemispheres:
		title = i.find("h3").text
		hemispheres_img = i.find("a", class_="itemLink product-item")["href"]
		
		# Visit the link that contains the full image website 
		browser.visit(hemispheres_url + hemispheres_img)
		
		# HTML Object
		image_html = browser.html
		web_info = BeautifulSoup(image_html, "html.parser")
		
		# Create full image url
		img_url = hemispheres_url + web_info.find("img", class_="wide-image")["src"]
		
		mars_info["title"] = title.strip()       
		mars_info["img_url"] = img_url
		
		hemispheres_info.append({"title" : title, "img_url" : img_url})

		mars_info["hemispheres_info"] = hemispheres_info
	
	# Close the browser after scraping
	browser.quit()
	
	return mars_info
	
	