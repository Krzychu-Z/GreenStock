package main

import (
	"github.com/gin-gonic/gin"
	"github.com/gin-contrib/cors"
	"encoding/json"
	"log"
	"net/http"
)

func getHistory(c *gin.Context) {
	dbJson := GetRequest("/statistics")

	dbStruct := InMinimumPriceHistory{}
	jsonErr := json.Unmarshal(dbJson, &dbStruct)
	if jsonErr != nil {
		log.Fatal(jsonErr)
	}

	outStruct, workerErr := CalculateTrend(dbStruct)
	if workerErr != nil {
		log.Fatal(workerErr)
	}

	c.IndentedJSON(http.StatusOK, outStruct)
}

func main() {
	router := gin.Default()
	router.Use(cors.Default())
    router.GET("/fullHistory", getHistory)
    router.Run("localhost:5001")
}