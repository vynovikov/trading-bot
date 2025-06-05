package api

import (
	"context"

	"github.com/trading-bot/stock-interactor/internal/entities"
)

type domain interface {
	GetCandles(
		ctx context.Context,
		historyEntity entities.History,
	) (
		<-chan []entities.Candle,
		<-chan error,
	)
}
