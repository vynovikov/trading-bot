package usecases

import "github.com/trading-bot/stock-interactor/internal/entities"

type transport interface {
	GetCandles(historyEntity entities.History) (<-chan []entities.Candle, error)
}
