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
	errChan chan<- error,
) error {
	semChan := make(chan struct{}, t.limit)
	wg := &sync.WaitGroup{}

	wg.Add(len(normalizedHistoryEntities))

	for _, historyEntity := range normalizedHistoryEntities {

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

	go func() {
		wg.Wait()
		close(resChan)
		close(errChan)
	}()

	return nil
}
