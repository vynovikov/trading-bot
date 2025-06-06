package entities

type Candle struct {
	OpenTime      float64
	Open          float64
	High          float64
	Low           float64
	Close         float64
	Volume        float64
	CloseTime     float64
	QuoteVolume   float64
	TradeCount    int32
	TakerBuyBase  float64
	TakerBuyQuote float64
}
