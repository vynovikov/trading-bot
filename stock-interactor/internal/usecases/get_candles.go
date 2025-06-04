package usecases

import "github.com/trading-bot/stock-interactor/internal/entities"

func (d domainStruct) GetCandles(
	historyEntity entities.History,
) (
	<-chan []entities.Candle,
	error,
) {
	return d.transport.GetCandles(historyEntity)
}
