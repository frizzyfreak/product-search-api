# **Scalable Product Search API**

## **1. Methodology**
<img src="https://user-images.githubusercontent.com/7460892/207003643-e03c8964-3f16-4a62-9a2d-b1eec5d8691f.png" width="80%" height="80%">

**Technology Stack**:
- **Backend Framework**: Go with Gin router [1]
- **Search Engine**: Elasticsearch v7 for full-text search [1][3]
- **Database**: PostgreSQL (implied in project description)
- **Tooling**: Docker for containerization [1][3]

## **2. Description**
<img src="https://user-images.githubusercontent.com/7460892/207003772-ba2061bc-f8fd-4479-ba42-4712328b7085.png" width="80%" height="80%">

A high-performance product search system featuring:
- RESTful API endpoint (`/products/search`) [1]
- Dynamic query construction with bool filters [1][2]
- Price range filtering and category matching [1][2]
- CLI interface for testing searches [2]
- Automated data seeding with random products [3]

## **3. Input / Output**
<img src="https://user-images.githubusercontent.com/7460892/207004091-8f67548d-50ac-49c3-b7cb-ef8ec18a6491.png" width="40%" height="40%">

**Input Parameters**:
