package transport

import (
	"context"
	"fmt"
	"strconv"
	"time"

	cerrors "github.com/cockroachdb/errors"
	resty "github.com/go-resty/resty/v2"
	"github.com/trading-bot/stock-interactor/internal/entities"
)

func fetch(ctx context.Context, history entities.History) ([]entities.Candle, error) {
	var raw [][]interface{}

	client := resty.New().
		SetTimeout(10 * time.Second).
		SetRetryCount(3).
		SetRetryWaitTime(1 * time.Second)

	_, err := client.R().
		SetContext(ctx).
		SetQueryParams(map[string]string{
			"symbol":    history.Symbol,
			"interval":  history.Interval,
			"startTime": fmt.Sprintf("%d", history.FromTimestamp),
			"endTime":   fmt.Sprintf("%d", history.ToTimestamp),
			"limit":     "1000",
		}).
		SetResult(&raw).
		Get("https://api.binance.com/api/v3/klines")

	if err != nil {
		return nil, cerrors.Wrap(err, "")
	}

	result := make([]entities.Candle, len(raw))
	for idx, val := range raw {
		if len(val) < 11 {
			return result, entities.ErrInvalidLength
		}

		openTime, ok := val[0].(float64)
		if !ok {
			return nil, cerrors.Wrap(entities.ErrInvalidOpenTime, "failed to parse open time")
		}

		closeTime, ok := val[6].(float64)
		if !ok {
			return nil, cerrors.Wrap(entities.ErrInvalidCloseTime, "failed to parse close time")
		}

		tradeFloat, ok := val[8].(float64)
		if !ok {
			return nil, cerrors.Wrap(entities.ErrInvalidTradeCount, "failed to parse trade count")
		}

		open, err := strconv.ParseFloat(val[1].(string), 64)
		if err != nil {
			return nil, cerrors.Wrap(err, "failed to parse open price")
		}

		high, err := strconv.ParseFloat(val[2].(string), 64)
		if err != nil {
			return nil, cerrors.Wrap(err, "failed to parse high price")
		}

		low, err := strconv.ParseFloat(val[3].(string), 64)
		if err != nil {
			return nil, cerrors.Wrap(err, "failed to parse low price")
		}

		closeVal, err := strconv.ParseFloat(val[4].(string), 64)
		if err != nil {
			return nil, cerrors.Wrap(err, "failed to parse close price")
		}

		volume, err := strconv.ParseFloat(val[5].(string), 64)
		if err != nil {
			return nil, cerrors.Wrap(err, "failed to parse volume")
		}

		quoteVolume, err := strconv.ParseFloat(val[7].(string), 64)
		if err != nil {
			return nil, cerrors.Wrap(err, "failed to parse quote volume")
		}

		takerBuyBase, err := strconv.ParseFloat(val[9].(string), 64)
		if err != nil {
			return nil, cerrors.Wrap(err, "failed to parse taker buy base")
		}

		takerBuyQuote, err := strconv.ParseFloat(val[10].(string), 64)
		if err != nil {
			return nil, cerrors.Wrap(err, "failed to parse taker buy quote")
		}

		result[idx] = entities.Candle{
			OpenTime:      openTime,
			Open:          open,
			High:          high,
			Low:           low,
			Close:         closeVal,
			Volume:        volume,
			CloseTime:     closeTime,
			QuoteVolume:   quoteVolume,
			TradeCount:    int32(tradeFloat),
			TakerBuyBase:  takerBuyBase,
			TakerBuyQuote: takerBuyQuote,
		}
	}

	return result, nil
}
