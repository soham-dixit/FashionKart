import requests
import os
import uuid
from bs4 import BeautifulSoup
import pandas as pd

# Global variable to count images
global count
count = 0

def download_image(image_url, string, save_directory='thumbnails'):
    """Downloads an image from the provided URL and saves it to the specified directory."""
    global count
    try:
        # Send a GET request to the image URL
        response = requests.get(image_url)
        response.raise_for_status()  # Check for any errors in the request

        # Generate a unique filename using UUID
        count += 1
        unique_filename = string + '.jpg'

        # Create the full path to save the image
        save_path = os.path.join(save_directory, unique_filename)

        # Save the image to the specified directory
        with open(save_path, 'wb') as file:
            file.write(response.content)

        return save_path  # Return the unique file path

    except Exception as e:
        return str(e)  # Handle any exceptions and return an error message


def get_title(soup):
    """Extracts the product title from the soup object."""
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string


def get_image_link(soup):
    """Extracts the image link from the soup object."""
    try:
        img_div = soup.find("div", attrs={"id": 'imgTagWrapperId'})
        image_link = img_div.find("img")['src']
    except (AttributeError, KeyError):
        image_link = ""
    return image_link


def get_price(soup):
    """Extracts the product price from the soup object."""
    try:
        price = soup.find("span", attrs={"class": 'a-price-whole'}).string.strip()
    except AttributeError:
        price = ""
    return price


def get_rating(soup):
    """Extracts the product rating from the soup object."""
    try:
        rating = soup.find("span", attrs={"class": 'a-size-base a-color-base'}).string.strip()
    except AttributeError:
        rating = ""
    return rating


def get_availability(soup):
    """Extracts the product availability status from the soup object."""
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()
    except AttributeError:
        available = "Not Available"
    return available


def get_product_details(query):
    """Scrapes product details from Amazon based on the search query."""
    URL = f"https://www.amazon.in/s?k={query}"
    HEADERS = {'User-Agent': '', 'Accept-Language': 'en-US, en;q=0.5'}
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    # print(soup)

    # Extracting product links
    links = soup.find_all("a", attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    links_list = [link.get('href') for link in links]

    product_details = []

    # Fetching details of the first three products
    for link in links_list[:3]:
        amazon_url = "https://www.amazon.in" + link
        HEADERS = {
            'User-Agent': 'Chrome/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        }
        webpage = requests.get(amazon_url, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")

        title = get_title(soup)
        price = get_price(soup)
        rating = get_rating(soup)
        availability = get_availability(soup)
        image_link = get_image_link(soup)

        if title:
            product_details.append({
                'title': title,
                'price': price,
                'rating': rating,
                'availability': availability,
                'image': image_link,
                'link': amazon_url
            })
         # Print product details to console

    # Convert to DataFrame and save as CSV
    amazon_df = pd.DataFrame(product_details)
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)

    if not amazon_df.empty:
        # Get details of the first product
        first_product = amazon_df.iloc[0]

        # Download product thumbnail
        thumbnail_url = first_product['image']
        unique_path = download_image(thumbnail_url, query)

        # Format product details
        product_details = f"""Product Name: {first_product['title']}
Product Link: {first_product['link']}
Current Price: ₹{first_product['price']}
Availability: {first_product['availability']}
Clothing: {query}"""

        return unique_path, product_details
    else:
        return None, "No product details found."


# Example usage
search_string = "White Tshirt"
thumbnail, details = get_product_details(search_string)


if thumbnail and details:
    print("Thumbnail URL:", thumbnail)
    print("Product Details:")
    print(details)
else:
    print("No results found for the search string:", search_string)
