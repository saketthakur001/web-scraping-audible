import requests
from bs4 import BeautifulSoup

# Send a GET request to the URL of this page
def generate_link(page=1, audible_programs="20956260011", author_author="", keywords="", narrator="full-cast", publisher="", sort="review-rank", title=""):
  base_url = "https://www.audible.com/search?"
  params = {
    "audible_programs": audible_programs,
    "author_author": author_author,
    "keywords": keywords,
    "narrator": narrator,
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


response = requests.get(generate_link())



# # Create a soup object from the response content
# soup = BeautifulSoup(response.content, 'html.parser')

# print(soup.prettify())

# # Find all the elements that have the class 'bc-list-item productListItem'
# items = soup.find_all('div', class_='bc-list-item productListItem')

# # Loop through the items and get the title and rating of each audiobook
# for item in items:
#     # Find the element that has the class 'bc-link bc-color-link' and get its text
#     title = item.find('a', class_='bc-link bc-color-link').text.strip()
#     # Find the element that has the class 'bc-text bc-size-small bc-color-secondary' and get its text
#     rating = item.find('span', class_='bc-text bc-size-small bc-color-secondary').text.strip()
#     # Print the title and rating
#     print(title)
#     print(rating)
#     # print()