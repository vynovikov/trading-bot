package transport

import "github.com/trading-bot/stock-interactor/internal/config"

type transportStruct struct {
}

func New(cfg config.ENV) transportStruct {
	return transportStruct{}
}
