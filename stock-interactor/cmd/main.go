package main

import (
	"context"
	"fmt"
	"log/slog"
	"os"
	"os/signal"
	"syscall"

	"github.com/trading-bot/stock-interactor/internal/application"
	"github.com/trading-bot/stock-interactor/internal/config"
	pkgLogger "github.com/trading-bot/stock-interactor/pkg/logger"
)

func main() {
	ctx, cancel := signal.NotifyContext(
		context.Background(),
		syscall.SIGINT,
		syscall.SIGTERM,
	)
	defer cancel()
	logger := slog.New(pkgLogger.NewPrettyHandler(os.Stdout, &slog.HandlerOptions{
		Level: slog.LevelDebug,
	}))

	cfg, err := config.Parse()
	if err != nil {
		logger.ErrorContext(ctx, "failed to parse config", slog.String("error", fmt.Sprintf("%+v", err)))

		return
	}

	err = application.Start(ctx, cfg, logger)
	if err != nil {
		logger.ErrorContext(ctx, "failed to start application", slog.Any("|error", err))

		return
	}
}
