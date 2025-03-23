import requests
import argparse
import json

# Elasticsearch server URL
ES_URL = "http://localhost:9200/products/_search"

def search_products(query=None, min_price=None, max_price=None, category=None):
    """Search products in Elasticsearch based on user input."""
    
    # Build the search query dynamically
    search_query = {"query": {"bool": {"must": [], "filter": []}}}

    if query:
        search_query["query"]["bool"]["must"].append({"match": {"name": query}})
    
    if min_price or max_price:
        price_filter = {}
        if min_price:
            price_filter["gte"] = min_price
        if max_price:
            price_filter["lte"] = max_price
        search_query["query"]["bool"]["filter"].append({"range": {"price": price_filter}})

    if category:
        search_query["query"]["bool"]["filter"].append({"term": {"category": category}})
    
    # Send request to Elasticsearch
    response = requests.get(ES_URL, headers={"Content-Type": "application/json"}, data=json.dumps(search_query))
    
    if response.status_code != 200:
        print(f"❌ Error: {response.text}")
        return

    # Parse results
    results = response.json()
    hits = results.get("hits", {}).get("hits", [])

    if not hits:
        print("No products found.")
        return

    print("\n🔍 Search Results:")
    for hit in hits:
        product = hit["_source"]
        print(f"✅ {product['name']} - ₹{product['price']} [{product['category']}]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI tool to search products in Elasticsearch")
    
    parser.add_argument("-q", "--query", type=str, help="Search query (product name)")
    parser.add_argument("-min", "--min_price", type=float, help="Minimum price")
    parser.add_argument("-max", "--max_price", type=float, help="Maximum price")
    parser.add_argument("-c", "--category", type=str, help="Filter by category")

    args = parser.parse_args()

    search_products(args.query, args.min_price, args.max_price, args.category)
