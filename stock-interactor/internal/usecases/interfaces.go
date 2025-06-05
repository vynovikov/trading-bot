package usecases

import (
	"context"

	"github.com/trading-bot/stock-interactor/internal/entities"
)

type transport interface {
	GetCandles(
		ctx context.Context,
		historyEntity entities.History,
	) (
		<-chan []entities.Candle,
		<-chan error,
	)
}
