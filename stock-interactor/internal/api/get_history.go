package api

import (
	"fmt"
	"log"

	pb "github.com/trading-bot/stock-interactor/internal/api/pb"

	cerrors "github.com/cockroachdb/errors"
)

func (a API) GetHistory(req *pb.HistoryRequest, stream pb.HistoryService_GetHistoryServer) error {
	err1 := topLevel()

	fmt.Printf("detailed: %+v\n", err1)

	for range 3 {
		response := &pb.HistoryResponse{
			Candles: []*pb.Candle{
				{
					OpenTime: 10000,
					Open:     100.0,
					Close:    105.0,
					High:     110.0,
					Low:      95.0,
					Volume:   1000.0,
				},

				{
					OpenTime: 11000,
					Open:     200.0,
					Close:    205.0,
					High:     210.0,
					Low:      195.0,
					Volume:   1100.0,
				},
			},
		}
		if err := stream.Send(response); err != nil {
			log.Println("Error sending response:", err)
			return err
		}
	}
	return nil
}

func lowLevel() error {
	return cerrors.New("connection refused")
}

func midLevel() error {
	return cerrors.Wrap(lowLevel(), "could not fetch user profile")
}

func topLevel() error {
	return cerrors.Wrap(midLevel(), "HTTP request failed")
}
