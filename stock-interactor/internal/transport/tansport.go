package transport

import "github.com/trading-bot/stock-interactor/internal/config"

type transportStruct struct {
	limit int
}

func New(cfg config.ENV) transportStruct {
	return transportStruct{
		limit: cfg.BinanceCandlesLimit,
	}
}
