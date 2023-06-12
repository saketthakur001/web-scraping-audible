import re
import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import datetime
# import date

def get_authors(text, string=True):
  try:
    return text.split('by: ')[1]#.split(', ')
    
  except:
    # if string: return text.join(', ')
    return None #[None]

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
        return date.year+ date.month/12 + date.day/365
    # check if text is float or int
    elif text.isnumeric():
        return text


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

def scrape_all_details(page):
# Send a GET request to the page and parse the HTML content
  # response = requests.get(page)
  # soup = BeautifulSoup(response.content, "html.parser")

  # Find all the elements that contain the product details
  products = soup.find_all("div", class_="bc-col-responsive bc-col-6")

  # Create an empty list to store the details
  details_list = []

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

# Loop through each product element and extract the details
  for product in products:
    # Try to find the title element and handle the exception if not found
    try:
      title = product.find("h3", class_="bc-heading").text.strip()
    except AttributeError:
      title = None
      continue
    # Try to find the subtitle element and handle the exception if not found
    try:
      # get the li element with class subtitle
      subtitle = product.find("li", class_="bc-list-item subtitle").text.strip()
    except AttributeError:
      subtitle = None

    # Try to find the author element and handle the exception if not found
    try:
      author = product.find("li", class_="authorLabel").text.strip()
    except AttributeError:
      author = None
    # Try to find the narrator element and handle the exception if not found
    try:
      narrator = product.find("li", class_="narratorLabel").text.strip()
    except AttributeError:
      narrator = None
    try:
      series = product.find("li", class_="seriesLabel").text.strip()
    except AttributeError:
      series = None
    try:
      length = product.find("li", class_="runtimeLabel").text.strip()
    except AttributeError:
      length = None
    try:
      release_date = product.find("li", class_="releaseDateLabel").text.strip() 
    except AttributeError:
      release_date = None
    try:
      language = product.find("li", class_="languageLabel").text.strip()
    except AttributeError:
      language = None

    try:
      ratings = product.find("li", class_="ratingsLabel").text.strip()
    except AttributeError:
      ratings = None

    # Try to find the summary element and handle the exception if not found
    try:
      summary = product.find("p", class_="bc-text").text.strip()
    except AttributeError:
      summary = None

    image = None

    # Try to find the link element and handle the exception if not found
    try:
      link = product.find("a", class_="bc-link bc-color-link").get("href")
    except AttributeError:
      link = None

    # Create a dictionary with the product details
    details_dict = {
      "title"        : title,
      "subtitle"     : subtitle,
      "author"       : author,
      "narrator"     : narrator,
      "series"       : series,
      "length"       : length,
      "release_date" : release_date,
      "language"     : language,
      "ratings"      : ratings,
      "vote"         : None,
      "summary"      : summary,
      "image"        : image, # Add this line
      "link"         : link # Add this line
    }
    # Format the values using strip and replace methods
    for key, value in details_dict.items():
      # Remove leading and trailing whitespaces
      if value is None: continue
      value = value.strip()
      # Replace multiple whitespaces with a single space using re.sub
      value = re.sub("\s+", " ", value)
      # Update the dictionary with the formatted value
      details_dict[key] = value
      
    # Append the dictionary to the list
    details_list.append(details_dict)
    try:
      details_dict['series'] = details_dict['series'].split('Series: ')[1]
    except:
      details_dict['series'] = None
    try:
      details_dict['author'] = details_dict['author'].split('By: ')[1]
    except:
      details_dict['author'] = None
    # narrator
    try:
      details_dict['narrator'] = details_dict['narrator'].split("Narrated by: ")[1]
    except:
      details_dict['narrator'] = None
    # modify length
    details_dict['length'] = hour_min_to_min(details_dict['length'])
    # language
    try:
      details_dict['language'] = details_dict['language'].split('Language: ')[1]
    except:
      details_dict['language'] = None
    # add vote
    details_dict['votes'] = extract_rating(details_dict['ratings'])[1]
    # modify ratings
    details_dict['ratings'] = extract_rating(details_dict['ratings'])[0]
    # modify release date
    details_dict['release_date'] = string_to_date(details_dict['release_date'])

  # add cover image to the dictionary in the list
  for i in range(len(details_list)):
    details_list[i]["image"] = cover_image[i]

  # Return the list with all the details
  return details_list
# Define a class for the database operations
class AudibleDB:

    # Define a method to create the database and table
    def create_db(self):

        # Connect to the database file or create it if it does not exist
        self.conn = sqlite3.connect("audible.db")

        # Create a cursor object to execute SQL commands
        self.cur = self.conn.cursor()

        # Create a table called audiobooks with the following columns and data types
        # Create a table called audiobooks with the following columns and data types
        self.cur.execute("""CREATE TABLE IF NOT EXISTS audiobooks (
                        title TEXT,
                        subtitle TEXT,
                        author TEXT,
                        narrator TEXT,
                        series TEXT,
                        length INTEGER,
                        release_date TEXT,
                        language TEXT,
                        summary TEXT,
                        image TEXT,
                        link TEXT PRIMARY KEY,
                        ratings REAL,
                        votes INTEGER
                    )
                    """)


        # Commit the changes to the database
        self.conn.commit()

    # Define a method to insert data into the table
    def insert_data(self, data):

        # Loop through each item in the data list
        for item in data:
            # print(item)
            # Extract the values from the dictionary
            title = item["title"]
            subtitle = item["subtitle"]
            author = item["author"]
            narrator = item["narrator"]
            series = item["series"]
            length = item["length"]
            release_date = item["release_date"]
            language = item["language"]
            summary = item["summary"]
            image = item["image"]
            link = item["link"]
            ratings = item["ratings"]
            votes = item["votes"]
            # votes = item.get("votes", 0) # This will return 0 if "votes" is not in item
            # Insert the values into the table using placeholders and a tuple if it already doesn't exist
            self.cur.execute("""INSERT OR IGNORE INTO audiobooks VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                                ON CONFLICT(link) DO NOTHING;
                                """,
                             (title, subtitle, author, narrator, series, length, release_date, language, summary, image, link, ratings, votes))
                             # print if data is inserted

        # Commit the changes to the database
        self.conn.commit()

    def read_data(self, **kwargs):
        # Define the base query
        query = "SELECT * FROM audiobooks WHERE 1=1"

        # Define the parameters for the query
        params = []

        # Add the filters to the query and parameters
        if kwargs.get("author"):
            query += " AND author=?"
            params.append(kwargs["author"])
        if kwargs.get("narrator"):
            query += " AND narrator=?"
            params.append(kwargs["narrator"])
        if kwargs.get("series"):
            query += " AND series=?"
            params.append(kwargs["series"])
        if kwargs.get("language"):
            query += " AND language=?"
            params.append(kwargs["language"])
        if kwargs.get("min_length"):
            query += " AND length>=?"
            params.append(kwargs["min_length"])
        if kwargs.get("min_rating"):
            query += " AND ratings>=?"
            params.append(kwargs["min_rating"])
        if kwargs.get("min_votes"):
            query += " AND votes>=?"
            params.append(kwargs["min_votes"])
        if kwargs.get("search"):
            search_terms = kwargs["search"].split()
            for term in search_terms:
                query += " AND (title LIKE ? OR subtitle LIKE ? OR author LIKE ? OR narrator LIKE ? OR summary LIKE ?)"
                params.extend(["%{}%".format(term)] * 5)

        # Add the sorting to the query
        sort_by = kwargs.get("sort_by", "title")
        sort_order = kwargs.get("sort_order", "ASC")
        query += " ORDER BY {} {}".format(sort_by, sort_order)

        # Execute the query and get the results
        self.cur.execute(query, params)
        results = self.cur.fetchall()

        # Return the results
        return results

    # Define a method to close the connection to the database
    def close_db(self):
        self.conn.close()
# data = scrape_all_details(generate_link())
# request = requests.get(generate_link())
# soup = BeautifulSoup(request.text, "html.parser")

data = scrape_all_details(generate_link())



# Create an instance of the class
db = AudibleDB()

# Call the create_db method to create the database and table
db.create_db()

# Call the insert_data method to insert the data into the table
db.insert_data(data)
# db.close_db()