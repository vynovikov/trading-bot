package api

import "github.com/trading-bot/stock-interactor/internal/entities"

type domain interface {
	GetCandles(historyEntity entities.History) (<-chan []entities.Candle, error)
}
