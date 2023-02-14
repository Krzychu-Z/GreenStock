package main

type InMinimumPriceHistory struct {
	ResourcePrices []struct {
		Time   string `json:"time"`
		Prices []struct {
			Resource string  `json:"resource"`
			Price    float64 `json:"price"`
		} `json:"prices"`
	} `json:"ResourcePrices"`
}

type OutMinimumPriceHistory struct {
	ResourcePrices []struct {
		Time   string `json:"time"`
		Prices []struct {
			Resource string  `json:"resource"`
			Price    float64 `json:"price"`
		} `json:"prices"`
	} `json:"ResourcePrices"`
	Trends []struct {
		Resource string `json:"resource"`
		Difference float64 `json:"difference"`
		Trend    string `json:"trend"`
	} `json:"Trends"`
}