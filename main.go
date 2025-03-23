package main

import (
	"bytes"
	"context"
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/elastic/go-elasticsearch/v7"
	"github.com/gin-gonic/gin"
)

type Product struct {
	ID       string  `json:"id"`
	Name     string  `json:"name"`
	Price    float64 `json:"price"`
	Category string  `json:"category"`
}

func main() {
	es, err := elasticsearch.NewDefaultClient()
	if err != nil {
		log.Fatalf("Error creating the client: %s", err)
	}

	router := gin.Default()

	router.GET("/products/search", func(c *gin.Context) {
		query := c.Query("query")
		minPriceStr := c.Query("minPrice")
		maxPriceStr := c.Query("maxPrice")
		category := c.Query("category")

		var minPrice, maxPrice float64
		var err error
		if minPriceStr != "" {
			minPrice, err = strconv.ParseFloat(minPriceStr, 64)
			if err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid minPrice"})
				return
			}
		}
		if maxPriceStr != "" {
			maxPrice, err = strconv.ParseFloat(maxPriceStr, 64)
			if err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid maxPrice"})
				return
			}
		}

		searchQuery := map[string]interface{}{
			"query": map[string]interface{}{
				"bool": map[string]interface{}{
					"must": []map[string]interface{}{
						{"match": map[string]interface{}{"name": query}},
					},
					"filter": []map[string]interface{}{
						{"range": map[string]interface{}{"price": map[string]interface{}{"gte": minPrice, "lte": maxPrice}}},
						{"term": map[string]interface{}{"category": category}},
					},
				},
			},
		}

		var buf bytes.Buffer
		if err := json.NewEncoder(&buf).Encode(searchQuery); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to encode search query"})
			return
		}

		res, err := es.Search(
			es.Search.WithContext(context.Background()),
			es.Search.WithIndex("products"),
			es.Search.WithBody(&buf),
			es.Search.WithPretty(),
		)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		defer res.Body.Close()

		var r map[string]interface{}
		if err := json.NewDecoder(res.Body).Decode(&r); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to parse Elasticsearch response"})
			return
		}

		hits, ok := r["hits"].(map[string]interface{})["hits"].([]interface{})
		if !ok {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Invalid response format from Elasticsearch"})
			return
		}

		var products []Product
		for _, hit := range hits {
			hitMap := hit.(map[string]interface{})
			source := hitMap["_source"].(map[string]interface{})

			product := Product{
				ID:       hitMap["_id"].(string),
				Name:     source["name"].(string),
				Price:    source["price"].(float64),
				Category: source["category"].(string),
			}
			products = append(products, product)
		}

		c.JSON(http.StatusOK, products)
	})

	router.Run(":8080")
}
