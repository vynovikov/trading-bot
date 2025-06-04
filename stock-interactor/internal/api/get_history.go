package api

import (
	pb "github.com/trading-bot/stock-interactor/internal/api/pb"

	cerrors "github.com/cockroachdb/errors"
)

func (a API) GetHistory(
	req *pb.HistoryRequest,
	stream pb.HistoryService_GetHistoryServer,
) error {
	candlesChan, err := a.domain.GetCandles(unmarshalHistoryRequest(req))
	if err != nil {
		return cerrors.Wrap(err, "failed to get candles")
	}

	for candles := range candlesChan {
		if err := stream.Send(marshalHistoryResponse(candles)); err != nil {
			return cerrors.Wrap(err, "failed to send candle")
		}
	}

	return nil
}
