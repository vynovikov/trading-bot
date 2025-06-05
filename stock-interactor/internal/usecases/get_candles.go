package usecases

import (
	"context"

	"github.com/trading-bot/stock-interactor/internal/entities"
)

func (d domainStruct) GetCandles(
	ctx context.Context,
	historyEntity entities.History,
) (
	<-chan []entities.Candle,
	<-chan error,
) {
	return d.transport.GetCandles(ctx, historyEntity)
}
