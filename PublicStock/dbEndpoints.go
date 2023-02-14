package main

import (
	"errors"
	"net/http"
	"time"
	"log"
	"io/ioutil"
//	"crypto/tls"
)


func GetRequest(endpoint string) []byte  {

/*	cert, err := tls.LoadX509KeyPair("cert.crt", "private.key")
	if err != nil {
		log.Fatal(err)
	}

	transport := &http.Transport{
		TLSClientConfig: &tls.Config{
			Certificates: []tls.Certificate{cert},
		},
	}
*/
	dbClient := http.Client{
		Timeout: time.Second * 10,
//		Transport: transport,
	}

	req, err := http.NewRequest(http.MethodGet, "http://localhost:5000" + endpoint, nil)
	if err != nil {
		log.Fatal(err)
	}

	res, getErr := dbClient.Do(req)
	if getErr != nil {
		log.Fatal(getErr)
	}

	if res.Body != nil {
		defer res.Body.Close()
	}

	body, readErr := ioutil.ReadAll(res.Body)
	if readErr != nil {
		log.Fatal(readErr)
	}

	return body

	/*
		THIS IS HOW UNMARSHALLING SHOULD LOOK LIKE IN GO

		struct1 := struct{}
		jsonErr := json.Unmarshal(body, &struct1)
		if jsonErr != nil {
			log.Fatal(jsonErr)
		}
	*/
}

func CalculateTrend(dataDump InMinimumPriceHistory) (OutMinimumPriceHistory, error) {
	length := len(dataDump.ResourcePrices)
	currentRecord := dataDump.ResourcePrices[length - 1].Prices
	previousRecord := dataDump.ResourcePrices[length - 2].Prices

	if len(currentRecord) != len(previousRecord) {
		return  OutMinimumPriceHistory{}, errors.New("[Abort] Corrupt JSON arrived: latest record and the record before that do not have matching lengths")
	}

	result := OutMinimumPriceHistory{}

	for i := 0; i < len(currentRecord); i++ {
		if currentRecord[i].Price >= previousRecord[i].Price {
			result.ResourcePrices = append(result.ResourcePrices, struct {
				Time   string `json:"time"`
				Prices []struct {
					Resource string  `json:"resource"`
					Price    float64 `json:"price"`
				} `json:"prices"`
			}{
				Time: dataDump.ResourcePrices[length - 1].Time,
				Prices: []struct {
					Resource string  `json:"resource"`
					Price    float64 `json:"price"`
				}{ 
					currentRecord[i],
				},
			})
		
			result.Trends = append(result.Trends, struct {
				Resource string `json:"resource"`
				Trend    string `json:"trend"`
			}{
				Resource: currentRecord[i].Resource,
				Trend:    "green",
			})
		} else {
			result.ResourcePrices = append(result.ResourcePrices, struct {
				Time   string `json:"time"`
				Prices []struct {
					Resource string  `json:"resource"`
					Price    float64 `json:"price"`
				} `json:"prices"`
			}{
				Time: dataDump.ResourcePrices[length - 1].Time,
				Prices: []struct {
					Resource string  `json:"resource"`
					Price    float64 `json:"price"`
				}{ 
					currentRecord[i],
				},
			})
		
			result.Trends = append(result.Trends, struct {
				Resource string `json:"resource"`
				Trend    string `json:"trend"`
			}{
				Resource: currentRecord[i].Resource,
				Trend:    "red",
			})
		}
	}

	return result, nil
}