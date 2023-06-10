import requests
from bs4 import BeautifulSoup

# Send a GET request to the URL of this page
def generate_link(page=1, audible_programs="20956260011", author_author="", keywords="", narrator="full-cast", publisher="", sort="review-rank", title="", pageSize=100):
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


def scrape_all_details(page):
  # Send a GET request to the page and parse the HTML content
  response = requests.get(page)
  soup = BeautifulSoup(response.content, "html.parser")

  # Find all the elements that contain the product details
  products = soup.find_all("div", class_="bc-col-responsive bc-col-6")

  # Create an empty list to store the details
  details_list = []

  # Loop through each product element and extract the details
  for product in products:
    # Try to find the title element and handle the exception if not found
    try:
      title = product.find("h3", class_="bc-heading").text.strip()
    except AttributeError:
      title = "N/A"
    # Try to find the subtitle element and handle the exception if not found
    try:
      subtitle = product.find("span", class_="subtitle").text.strip()
    except AttributeError:
      subtitle = "N/A"
    # Try to find the author element and handle the exception if not found
    try:
      author = product.find("li", class_="authorLabel").text.strip()
    except AttributeError:
      author = "N/A"
    # Try to find the narrator element and handle the exception if not found
    try:
      narrator = product.find("li", class_="narratorLabel").text.strip()
    except AttributeError:
      narrator = "N/A"
    try:
      series = product.find("li", class_="seriesLabel").text.strip()
    except AttributeError:
      series = "N/A"
    try:
      length = product.find("li", class_="runtimeLabel").text.strip()
    except AttributeError:
      length = "N/A"
    try:
      release_date = product.find("li", class_="releaseDateLabel").text.strip() 
    except AttributeError:
      release_date = "N/A"
    try:
      language = product.find("li", class_="languageLabel").text.strip()
    except AttributeError:
      language = "N/A"

    try:
      ratings = product.find("li", class_="ratingsLabel").text.strip()
    except AttributeError:
      ratings = "N/A"

    # Try to find the summary element and handle the exception if not found
    try:
      summary = product.find("p", class_="bc-text").text.strip()
    except AttributeError:
      summary = "N/A"
    # # Try to find the image element and handle the exception if not found
    # try:
    #   image = product.find("img", class_="bc-pub-block bc-image-inset-border js-only-element").get("src")
    # except AttributeError:
    #   image = "N/A"
    # # Try to find the image element and handle the exception if not found
    # try:
    #   image = product.find("img", attrs={"class": "bc-pub-block bc-image-inset-border js-only-element"}).get("src")
    # except AttributeError:
    #   image = "N/A"

      # Try to find the image element and handle the exception if not found
    try:
      image = product.find("img", class_=["bc-pub-block", "bc-image-inset-border", "js-only-element"]).get("src")
    except AttributeError:
      image = "N/A"


    # Try to find the link element and handle the exception if not found
    try:
      link = product.find("a", class_="bc-link bc-color-link").get("href")
    except AttributeError:
      link = "N/A"

    # Create a dictionary with the product details
    details_dict = {
      "title": title,
      "subtitle": subtitle,
      "author": author,
      "narrator": narrator,
      "series": series,
      "length": length,
      "release_date": release_date,
      "language": language,
      "ratings": ratings,
      "summary": summary,
      "image": image, # Add this line
      "link": link # Add this line
    }

    # Format the values using strip and replace methods
    for key, value in details_dict.items():
      # Remove leading and trailing whitespaces
      value = value.strip()
      # Replace multiple whitespaces with a single space using re.sub
      value = re.sub("\s+", " ", value)
      # Update the dictionary with the formatted value
      details_dict[key] = value

    # Append the dictionary to the list
    details_list.append(details_dict)

  # Return the list of details
  return details_list



# data = scrape_all_details()



data = scrape_all_details(generate_link())

# <img id="" class="bc-pub-blockbc-image-inset-border js-only-element" src="https://m.media-amazon.com/images/I/51Xt2BYA5vL._SL500_.jpg" loading="lazy" alt="We're Alive: A Story of Survival, the Third Season Audiobook By Kc Wayland cover art" width="100%" srcset="https://m.media-amazon.com/images/I/51Xt2BYA5vL._SL250_.jpg 1x, https://m.media-amazon.com/images/I/51Xt2BYA5vL._SL500_.jpg2x">
