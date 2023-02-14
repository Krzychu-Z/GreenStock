package GreenStock

type inMinimumPriceHistory struct {
	ResourcePrices []struct {
		Time   string `json:"time"`
		Prices []struct {
			Resource string  `json:"resource"`
			Price    float64 `json:"price"`
		} `json:"prices"`
	} `json:"ResourcePrices"`
}

type outMinimumPriceHistory struct {
	ResourcePrices []struct {
		Time   string `json:"time"`
		Prices []struct {
			Resource string  `json:"resource"`
			Price    float64 `json:"price"`
		} `json:"prices"`
	} `json:"ResourcePrices"`
	Trends []struct {
		Resource string `json:"resource"`
		Trend    string `json:"trend"`
	} `json:"Trends"`
}