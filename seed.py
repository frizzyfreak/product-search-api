import requests
import random
import json
import time

# Elasticsearch server URL
ES_URL = "http://localhost:9200/products/_doc"

# Sample product categories and names
categories = {
    "Electronics": ["Bluetooth Speaker", "Wireless Headphones", "Smartphone", "Smartwatch"],
    "Computers": ["Gaming Mouse", "Mechanical Keyboard", "Laptop", "Graphics Card"],
    "Footwear": ["Running Shoes", "Hiking Boots", "Sneakers", "Sandals"],
}

def generate_random_product():
    """Generate a random product with a name, category, and price."""
    category = random.choice(list(categories.keys()))
    name = random.choice(categories[category])
    price = round(random.uniform(1000, 20000), 2)  # Price between 1000 and 20000

    return {
        "name": name,
        "price": price,
        "category": category
    }

def index_product(product):
    """Insert a product into Elasticsearch."""
    response = requests.post(ES_URL, headers={"Content-Type": "application/json"}, data=json.dumps(product))

    if response.status_code in [200, 201]:
        print(f"✅ Inserted: {product['name']} (₹{product['price']}) [{product['category']}]")
    else:
        print(f"❌ Failed to insert: {product['name']} | Error: {response.text}")

if __name__ == "__main__":
    num_products = 10  # Change this number to insert more products

    for _ in range(num_products):
        product = generate_random_product()
        index_product(product)
        time.sleep(0.5)  # Slight delay to avoid overwhelming Elasticsearch

    print("🎯 Random Products Added to Elasticsearch!")
