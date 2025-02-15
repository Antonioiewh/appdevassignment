import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_ebay_estimated_price(product_title, condition):
    condition_map = {
        "Frequently used": "3000",
        "Barely used": "1000",
        "Used daily": "3000"
    }
    ebay_condition_id = condition_map.get(condition)
    if not ebay_condition_id:
        print(f"Condition '{condition}' not recognized.")
        return None
    url = f"https://www.ebay.com/sch/i.html?_nkw={urllib.parse.quote(product_title)}"
    params = {
        'condition': ebay_condition_id
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            print("Failed to reach eBay")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        price_elements = soup.find_all('span', class_='s-item__price')

        prices = []
        for element in price_elements:
            text = element.get_text().strip()
            if text == "$20.00":
                continue

            if text.startswith("$"):
                try:
                    price = float(text.replace("US", "").replace("$", "").split("to")[0].replace(",", "").strip())
                    prices.append(price)
                except ValueError:
                    continue

        if not prices:
            print("No valid prices found on eBay")
            return None  # Now correctly returns None instead of 20

        avg_price = sum(prices) / len(prices)
        final_price = format(round(avg_price, 2), ".2f")
        print(f"Final eBay price: {final_price}")  # Debugging line
        return final_price

    except Exception as e:
        print(f"Error scraping eBay for '{product_title}': {e}")
        return None


def get_amazon_estimated_price(product_title):
    query = urllib.parse.quote(product_title)
    url = f"https://www.amazon.com/s?k={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print("Could not reach")
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        # Amazon often uses spans with the class 'a-offscreen' for prices.
        price_elements = soup.find_all("span", class_="a-offscreen")
        prices = []
        for el in price_elements:
            text = el.get_text().strip()  # e.g. "$129.99"
            if text.startswith("$"):
                try:
                    price = float(text.replace("$", "").replace(",", "").strip())
                    prices.append(price)
                except ValueError:
                    continue
        if prices:
            avg_price = sum(prices) / len(prices)
            return round(avg_price, 2)
        return None
    except Exception as e:
        print(f"Error scraping Amazon for '{product_title}': {e}")
        return None

#amazon description does not work as amazon does not allow for web scraping
#          {% if estimated_amazon_price %}
#          <p>Amazon Estimated Price: ${{ estimated_amazon_price }}</p>
#          <div>
#            <a href="https://www.amazon.com" target="_blank" style="margin-right: 10px;">
#              <img src="{{ url_for('static', filename='amazon_logo.png') }}" alt="Amazon Logo" style="height: 30px;">
#            </a>
#          </div>
#        {% else %}
#          <p>Amazon price information is not available</p>
#        {% endif %}