package api

import (
	"github.com/trading-bot/stock-interactor/internal/api/pb"
	"github.com/trading-bot/stock-interactor/internal/entities"
)

func unmarshalHistoryRequest(req *pb.HistoryRequest) entities.History {
	if req == nil {
		return entities.History{}
	}
	return entities.History{
		Symbol:        req.GetSymbol(),
		Interval:      req.GetInterval(),
		FromTimestamp: req.GetFromTimestamp(),
		ToTimestamp:   req.GetToTimestamp(),
	}
}

func marshalHistoryResponse(candles []entities.Candle) *pb.HistoryResponse {
	if len(candles) == 0 {
		return &pb.HistoryResponse{}
	}

	pbCandles := make([]*pb.Candle, len(candles))
	for i, candle := range candles {
		pbCandles[i] = marshalCandle(candle)
	}

	return &pb.HistoryResponse{
		Candles: pbCandles,
	}
}

func marshalCandle(candle entities.Candle) *pb.Candle {
	return &pb.Candle{
		Open:   candle.Open,
		Close:  candle.Close,
		High:   candle.High,
		Low:    candle.Low,
		Volume: candle.Volume,
	}
}
