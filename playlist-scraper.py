"""
author: Kamesh Kotwani
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sys

try:
  USERNAME= sys.argv[1]
except:
  print("Please input username of youtube_channel")
  print("exiting...")
  sys.exit()

try:
  opts = webdriver.ChromeOptions()
  opts.headless=True
  driver = webdriver.Chrome(options=opts)

  # getting the body
  driver.get(f"https://www.youtube.com/c/{USERNAME}/playlists")


  # getting the scroll height
  last_height = driver.execute_script("return window.scrollY")

  # scrolling page till the end
  while True:
      print(last_height)
      driver.execute_script(f"window.scrollTo({last_height}, document.body.scrollHeight+10000);")

      # Wait to load the page.
      time.sleep(5)
      new_height = driver.execute_script("return window.scrollY")

      if new_height == last_height:
          break
      else:
          last_height = new_height
      
      # stopping for content to load
      time.sleep(5)

  # getting content of the page
  content = driver.page_source.encode('utf-8').strip()
  # creating soup
  soup = BeautifulSoup(content,'lxml')


  # getting all the titles of the videos
  titles = soup.find_all('a',id='video-title')

  # writing the videos into a file
  playlists = dict() 
  for title in titles:
    playlists[title.text] = "https://www.youtube.com"+title['href']

  with open(f'{USERNAME}.txt','w+',encoding='utf') as fp:
    for k,v in playlists.items():
      fp.write(f"{k} - {v}\n")

    
except Exception as e:
  print(e)
  pass

