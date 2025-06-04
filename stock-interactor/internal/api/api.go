package api

import (
	"log/slog"

	"github.com/trading-bot/stock-interactor/internal/api/pb"
	"github.com/trading-bot/stock-interactor/internal/config"
)

type API struct {
	pb.UnimplementedHistoryServiceServer
	domain domain
	logger *slog.Logger
}

func New(
	domain domain,
	cfg config.ENV,
	logger *slog.Logger,
) API {
	return API{
		domain: domain,
		logger: logger,
	}
}

var _ pb.HistoryServiceServer = (*API)(nil)
