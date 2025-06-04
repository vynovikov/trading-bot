package transport

import (
	"context"
	"sync"

	"github.com/trading-bot/stock-interactor/internal/entities"
)

func (t transportStruct) FetchParallel(
	ctx context.Context,
	normalizedHistoryEntities []entities.History,
	resChan chan<- []entities.Candle,
) error {
	semChan := make(chan struct{}, t.limit)
	errChan := make(chan error, len(normalizedHistoryEntities))
	wg := &sync.WaitGroup{}

	for _, historyEntity := range normalizedHistoryEntities {
		wg.Add(1)

		go func(history entities.History) {
			defer wg.Done()

			select {
			case semChan <- struct{}{}:
				defer func() { <-semChan }()

				result, err := fetch(ctx, history)
				if err != nil {
					errChan <- err
					return
				}

				resChan <- result
			case <-ctx.Done():
				errChan <- ctx.Err()

			}
		}(historyEntity)
	}
	wg.Wait()
	close(resChan)
	close(errChan)

	return nil
}
