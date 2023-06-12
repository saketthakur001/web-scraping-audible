import re
import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import datetime

def get_authors(text, string=True):
  try:
    return text.split('by: ')[1].split(', ')
  except:
    if string: return text.join(', ')
    return  [None]

# Send a GET request to the URL of this page
def generate_link(page=1, audible_programs="20956260011", author_author="", keywords="", narrator="full-cast", publisher="", sort="review-rank", title="", pageSize=50):
  base_url = "https://www.audible.com/search?"
  params = {
    "audible_programs": audible_programs,
    "author_author": author_author,
    "keywords": keywords,
    "narrator": narrator,
    "pageSize": pageSize,
    "publisher": publisher,
    "sort": sort,
    "title": title,
    "ref": "a_search_l1_audible_programs_0",
    "pf_rd_p": "daf0f1c8-2865-4989-87fb-15115ba5a6d2",
    "pf_rd_r": "3CSM3Q3AG46QRQ0TVK0F",
    "pageLoadId": "dELu6hUurPGV8fAu",
    "creativeId": "9648f6bf-4f29-4fb4-9489-33163c0bb63e"
  }
  if page > 1:
    params["page"] = page
  query = "&".join([f"{key}={value}" for key, value in params.items()])
  return base_url + query



# convert string to date object
def string_to_date(text):
    '''
    Convert string to date object
    datetime.date
        year in float
        ex: 2013.2993150684931
    '''
    if text == None:
        return None
    elif 'Release date: ' in text:
        month, day, year = text.split('Release date: ')[1].split('-')
        year = "20"+year
        # month, day, year = map(int, text.split('-'))
        date =  datetime.date(int(year), int(month), int(day))
    # check if text is float or int
    elif text.isnumeric():
        return text
    return date.year+ date.month/12 + date.day/365

# convert string to date object
def extract_rating(string):
    if string == "Not rated yet" or string == None:
        return None, None
    string = string.split(' out of 5 stars ')
    rating = float(string[0])
    votes = int(string[1].split(' rating')[0].replace(',',''))
    return rating, votes


# convert string to date object
def extract_rating(string):
    if string == "Not rated yet" or string == None:
        return None, None
    string = string.split(' out of 5 stars ')
    rating = float(string[0])
    votes = int(string[1].split(' rating')[0].replace(',',''))
    return rating, votes


# hour and min to min
def hour_min_to_min(tim):
    if tim == None:
        return None
    elif 'min' not in tim:
        return int(tim.split('Length: ')[1].split(' hr')[0])*60
    elif 'hr' not in tim:
        return int(tim.split('Length: ')[1].split(' min')[0])
    else:
        hr = tim.split('Length: ')[1].split(' hr')[0]
        minute = tim.split("and ")[1].split(' min')[0]
    return int(hr)*60 + int(minute)


# Define a function to scrape all details from a page
def scrape_all_details(page):
  """Scrape product details from an Amazon page.

  Args:
    page (str): The URL of the page to scrape.

  Returns:
    list: A list of dictionaries containing product details.
  """
  # Send a GET request to the page and parse the HTML content
  # response = requests.get(page)
  # soup = BeautifulSoup(response.content, "html.parser")

  # Find all the elements that contain the product details
  products = soup.find_all("div", class_="bc-col-responsive bc-col-6")

  # Find all the image links
  img_tags = soup.find_all("img")
  # list of image
  urls = []
  # Loop through the img tags and get the src attribute of each one
  for i, img_tag in enumerate(img_tags):
    try:
      src = img_tag["src"]
      # print(src) # Print the image URL
      urls.append(src)

    except:
      src = None
      urls.append(src)
  # print(src) # Print the image URL
  cover_image = []
  for image_link in urls:
    if "https://m.media-amazon.com/images/I" in image_link or ".jpg" in image_link:
      # print(image_link)
      cover_image.append(image_link)
  if len(cover_image) % 10 != 0:
    print(f"Error: {len(cover_image)} images found")
    return None
  else:
    print(f"Success: {len(cover_image)} images found")


  # Create an empty list to store the details
  details_list = []

  # Loop through each product element and extract the details
  for product in products:
    # Initialize an empty dictionary to store the product details
    details_dict = {}

    # Try to find the title element and handle the exception if not found
    try:
      title = product.find("h3", class_="bc-heading").text.strip()
      details_dict["title"] = title
    except :
      # Assign None if title is not found
      details_dict["title"] = None

    # Try to find the subtitle element and handle the exception if not found
    try:
      subtitle = product.find("li", class_="bc-list-item subtitle").text.strip()
      details_dict["subtitle"] = subtitle
    except :
      # Assign None if subtitle is not found
      details_dict["subtitle"] = None

    # Try to find the author element and handle the exception if not found
    try:
      author = product.find("li", class_="authorLabel").text.strip()
      details_dict["author"] = author.split("By: ")[1]
    except :
      # Assign None if author is not found
      details_dict["author"] = None

    # Try to find the narrator element and handle the exception if not found
    try:
      narrator = product.find("li", class_="narratorLabel").text.strip()
      details_dict["narrator"] = narrator.split("Narrated by: ")[1]
    except :
      # Assign None if narrator is not found
      details_dict["narrator"] = None

    # Try to find the series element and handle the exception if not found
    try:
      series = product.find("li", class_="seriesLabel").text.strip()
      details_dict["series"] = series.split("Series: ")[1]
    except :
      # Assign None if series is not found
      details_dict["series"] = None

    # Try to find the length element and handle the exception if not found
    try:
      length = product.find("li", class_="runtimeLabel").text.strip()
      details_dict["length"] = hour_min_to_min(length)
    except :
      # Assign None if length is not found
      details_dict["length"] = None

    # Try to find the release date element and handle the exception if not found
    try:
      release_date = product.find("li", class_="releaseDateLabel").text.strip()
      details_dict["release_date"] = release_date.split("Release date: ")[1]
    except :
      # Assign None if release date is not found
      details_dict["release_date"] = None

    # Try to find the language element and handle the exception if not found
    try:
      language = product.find("li", class_="languageLabel").text.strip()
      details_dict["language"] = language.split("Language: ")[1]
    except :
      # Assign None if language is not found
      details_dict["language"] = None

    # Try to find the summary element and handle the exception if not found
    try:
      summary = product.find("p", class_="bc-text").text.strip()
      details_dict["summary"] = summary
    except :
      # Assign None if summary is not found
      details_dict["summary"] = None

    # Try to find the image element and handle the exception if not found
    try:
      image = product.find("img").get("src")
      details_dict["image"] = image
    except :
      # Assign None if image is not found
      details_dict["image"] = None

    # Try to find the link element and handle the exception if not found
    try:
      link = product.find("a", class_="bc-link bc-color-link").get("href")
      details_dict["link"] = link
    except :
      # Assign None if link is not found
      details_dict["link"] = None
    
    # Try to find the ratings element and handle the exception if not found
    try:
      ratings = product.find("li", class_="ratingsLabel").text.strip()
      details_dict["ratings"] = ratings
    except :
      # Assign None if ratings is not found
      details_dict["ratings"] = None

    # Format the values using strip and replace methods
    for key, value in details_dict.items():
      # Remove leading and trailing whitespaces
      try:
        value = value.strip()
              # Replace multiple whitespaces with a single space using re.sub
        value = re.sub("\s+", " ", value)
        # Update the dictionary with the formatted value
        details_dict[key] = value
      except :
        pass

    # Append the dictionary to the list
    if details_dict["title"] is not None:
      details_dict["ratings"], details_dict["votes"] = extract_rating(details_dict["ratings"])
      details_list.append(details_dict)

  # Add the image link to the dictionary
  for i in range(len(details_list)):
    details_list[i]["image"] = cover_image[i]

  # Return the list with all the details
  return details_list

# request = requests.get(generate_link())
# soup = BeautifulSoup(request.text, "html.parser")

data = scrape_all_details(generate_link())
# data[4]