package entities

import "errors"

var (
	ErrInvalidLength     = errors.New("invalid length")
	ErrInvalidOpenTime   = errors.New("invalid open time")
	ErrInvalidCloseTime  = errors.New("invalid close time")
	ErrInvalidTradeCount = errors.New("invalid trade count")
)
