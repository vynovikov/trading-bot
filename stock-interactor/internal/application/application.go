package application

import (
	"context"
	"log/slog"

	apiInteractor "github.com/trading-bot/stock-interactor/internal/api"
	"github.com/trading-bot/stock-interactor/internal/config"
	transportInteractor "github.com/trading-bot/stock-interactor/internal/transport"
	usecasesInteractor "github.com/trading-bot/stock-interactor/internal/usecases"
)

func Start(ctx context.Context, cfg config.ENV, logger *slog.Logger) error {
	interactorTransport := transportInteractor.New(cfg)
	interactorDomain := usecasesInteractor.New(interactorTransport)
	interactorAPI := apiInteractor.New(interactorDomain, cfg, logger)

	err := apiInteractor.Run(ctx, interactorAPI, cfg)
	if err != nil {
		return err
	}

	return nil
}
