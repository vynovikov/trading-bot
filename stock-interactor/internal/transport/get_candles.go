package transport

import (
	"context"

	"github.com/trading-bot/stock-interactor/internal/entities"
)

func (t transportStruct) GetCandles(
	ctx context.Context,
	historyEntity entities.History,
) (
	<-chan []entities.Candle,
	<-chan error,
) {

	normalizedHistoryEntities, err := Normalize(historyEntity, t.limit)

	if err != nil {
		errChan := make(chan error, 1)
		resChan := make(chan []entities.Candle, 1)
		errChan <- err
		close(resChan)
		close(errChan)

		return resChan, errChan
	}

	resChan := make(chan []entities.Candle, t.limit)
	errChan := make(chan error, len(normalizedHistoryEntities))

	err = t.FetchParallel(ctx, normalizedHistoryEntities, resChan, errChan)
	if err != nil {
		errChan <- err
		close(resChan)
		close(errChan)

		return resChan, errChan
	}

	return resChan, errChan
}
