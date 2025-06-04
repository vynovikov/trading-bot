package api

import (
	"context"
	"errors"
	"fmt"
	"log"
	"log/slog"
	"net"

	"github.com/trading-bot/stock-interactor/internal/api/pb"
	"github.com/trading-bot/stock-interactor/internal/config"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

func Run(
	ctx context.Context,
	api API,
	cfg config.ENV,
) error {
	lis, err := net.Listen("tcp", cfg.AddressGRPC)
	if err != nil {
		return fmt.Errorf("failed to listen: %v", err)
	}

	s := grpc.NewServer()
	pb.RegisterHistoryServiceServer(s, api)
	reflection.Register(s)

	go func() {
		log.Printf("gRPC server listening on %s", cfg.AddressGRPC)
		err := s.Serve(lis)
		if errors.Is(err, net.ErrClosed) {
			api.logger.InfoContext(ctx, "gRPC server closed gracefully")

			return
		}
		if err != nil {
			api.logger.ErrorContext(ctx, "failed to serve gRPC server", slog.String("error", fmt.Sprintf("%+v", err)))
		}
	}()

	<-ctx.Done()

	lis.Close()
	s.GracefulStop()

	return nil
}
