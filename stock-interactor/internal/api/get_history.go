package api

import (
	"sync"

	pb "github.com/trading-bot/stock-interactor/internal/api/pb"

	cerrors "github.com/cockroachdb/errors"
)

func (a API) GetHistory(
	req *pb.HistoryRequest,
	stream pb.HistoryService_GetHistoryServer,
) error {
	var errs []error

	defer func() {
		for _, err := range errs {
			a.logger.Info("GetHistory error", "error", err)
		}
	}()

	candlesChan, errChan := a.domain.GetCandles(stream.Context(), unmarshalHistoryRequest(req))

	wg := &sync.WaitGroup{}
	wg.Add(2)

	go func() {
		defer func() {
			wg.Done()
		}()
		for candles := range candlesChan {
			if err := stream.Send(marshalHistoryResponse(candles)); err != nil {
				errs = append(errs, cerrors.Wrap(err, "failed to close stream"))
			}

		}
	}()

	go func() {
		defer wg.Done()
		for err := range errChan {
			errs = append(errs, cerrors.Wrap(err, "failed to get candles"))
		}
	}()

	wg.Wait()

	return nil
}
