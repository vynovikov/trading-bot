package transport

import (
	"context"
	"time"

	"github.com/trading-bot/stock-interactor/internal/entities"
)

func (t transportStruct) GetCandles(
	historyEntity entities.History,
) (
	<-chan []entities.Candle,
	error,
) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	resChan := make(chan []entities.Candle, t.limit)

	normalizedHistoryEntities, err := Normalize(historyEntity, t.limit)
	if err != nil {
		return nil, err
	}

	err = t.FetchParallel(ctx, normalizedHistoryEntities, resChan)
	if err != nil {
		return nil, err
	}

	return resChan, nil
}
