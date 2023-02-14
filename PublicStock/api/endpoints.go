package GreenStock

import (
	"errors"
)


func calculateTrend(dataDump inMinimumPriceHistory) (outMinimumPriceHistory, error) {
	length := len(dataDump.ResourcePrices)
	currentRecord := dataDump.ResourcePrices[length - 1].Prices
	previousRecord := dataDump.ResourcePrices[length - 2].Prices

	if len(currentRecord) != len(previousRecord) {
		return  outMinimumPriceHistory{}, errors.New("[Abort] Corrupt JSON arrived: latest record and the record before that do not have matching lengths")
	}

	for i := 0; i < len(currentRecord); i++ {

	}
}