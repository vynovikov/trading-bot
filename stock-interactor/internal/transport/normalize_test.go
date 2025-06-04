package transport_test

import (
	"testing"

	"github.com/stretchr/testify/suite"
	"github.com/trading-bot/stock-interactor/internal/entities"
	"github.com/trading-bot/stock-interactor/internal/transport"
)

type historySuite struct {
	suite.Suite
}

func TestHistorySuite(t *testing.T) {
	suite.Run(t, new(historySuite))
}

func (s *historySuite) TestNormalize() {
	tt := []struct {
		name         string
		history      entities.History
		limit        int
		wantEntities []entities.History
		wantError    error
	}{
		{
			name: "0. Interval is in candles limit",
			history: entities.History{
				Symbol:        "AAPL",
				Interval:      "15m",
				FromTimestamp: 1617187200,
				ToTimestamp:   1617273600,
			},
			limit: 1000,
			wantEntities: []entities.History{
				{
					Symbol:        "AAPL",
					Interval:      "15m",
					FromTimestamp: 1617187200,
					ToTimestamp:   1617273600,
				},
			},
			wantError: nil,
		},
		{
			name: "1. Interval exceeds candles limit",
			history: entities.History{
				Symbol:        "AAPL",
				Interval:      "15m",
				FromTimestamp: 1617187200,
				ToTimestamp:   1618273600,
			},
			limit: 1000,
			wantEntities: []entities.History{
				{
					Symbol:        "AAPL",
					Interval:      "15m",
					FromTimestamp: 1617187200,
					ToTimestamp:   1618087200,
				},
				{
					Symbol:        "AAPL",
					Interval:      "15m",
					FromTimestamp: 1618087200,
					ToTimestamp:   1618273600,
				},
			},
			wantError: nil,
		},
	}
	for _, v := range tt {
		s.Run(v.name, func() {
			gotEntities, gotError := transport.Normalize(v.history, v.limit)
			if v.wantError != nil {
				s.Equal(v.wantError, gotError)
			}

			s.Equal(v.wantEntities, gotEntities)
		})
	}
}
