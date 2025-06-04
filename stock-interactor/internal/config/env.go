package config

import (
	envparse "github.com/caarlos0/env/v10"
	cerrors "github.com/cockroachdb/errors"
)

type ENV struct {
	AddressGRPC string `env:"ADDRESS_GRPC,required"`
}

func Parse() (ENV, error) {
	var cfg ENV
	if err := envparse.Parse(&cfg); err != nil {
		return ENV{}, cerrors.Wrapf(err, "failed to parse environment variables")
	}
	return cfg, nil
}
