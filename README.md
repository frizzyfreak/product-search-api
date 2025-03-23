
# **Scalable Product Search API**

## **1. Methodology**
![image](https://github.com/user-attachments/assets/350cfa35-6144-4547-ba2c-52b4ab1d7e82)



**Technology Stack**:
- **Backend Framework**: Go with Gin router [1]
- **Search Engine**: Elasticsearch v7 for full-text search [1][3]
- **Database**: PostgreSQL (implied in project description)
- **Tooling**: Docker for containerization [1][3]

## **2. Description**


A high-performance product search system featuring:
- RESTful API endpoint (`/products/search`) [1]
- Dynamic query construction with bool filters [1][2]
- Price range filtering and category matching [1][2]
- CLI interface for testing searches [2]
- Automated data seeding with random products [3]

## **3. Input / Output**


**Input Parameters**:
```
python cli.py -q "Wireless Headphones" -min 1000 -max 5000 -c Electronics[2]
```

**API Response**:
```
[
  {
    "id": "1", 
    "name": "Wireless Headphones",
    "price": 2999.99,
    "category": "Electronics"
  }
]
```

## **4. Live Link**
`http://localhost:8080/products/search` (Local deployment via Docker) [1][3]

## **5. Screenshot of the Interface**
![image](https://github.com/user-attachments/assets/710da719-f400-447f-afbc-d2490525033d)


*CLI interface showing search results [2]*

## **6. How to Run**
```
# Clone repository
git clone https://github.com/frizzyfreak/product-search-api
cd product-search-api

# Start containers
docker-compose up --build[1][3]

# Seed sample data (in new terminal)
python seed.py[3]

# Execute search
python cli.py -q "Gaming Mouse" -min 1000 -max 10000 -c Computers[2]
```

## **7. GitHub Repository**
Explore the full implementation:  
[https://github.com/frizzyfreak/product-search-api](https://github.com/frizzyfreak/product-search-api/tree/master)
