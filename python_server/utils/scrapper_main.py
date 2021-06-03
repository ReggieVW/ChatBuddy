# -*- coding: utf-8 -*-
from google_image_scrapper import GoogleImageScraper
import os

webdriver_path = os.getcwd()+"\\webdriver\\chromedriver.exe"
image_path = os.getcwd()+"\\images"
search_keys= ["angry elderly person face","Happy elderly person face", "Neutral elderly person face","sad elderly person face","Surprised elderly person face"]
number_of_images = 500
headless = False
min_resolution=(0,0)
max_resolution=(1920,1080)
for search_key in search_keys:
    image_scrapper = GoogleImageScraper(webdriver_path,image_path,search_key,number_of_images,headless,min_resolution,max_resolution)
    image_urls = image_scrapper.find_image_urls()
    image_scrapper.save_images(image_urls)
