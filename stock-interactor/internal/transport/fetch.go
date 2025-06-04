package transport

import (
	"context"
	"fmt"
	"strconv"
	"time"

	"github.com/go-resty/resty/v2"
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
		return nil, err
	}

	result := make([]entities.Candle, 0, len(raw))
	for idx, val := range raw {
		if len(val) < 7 {
			return result, entities.ErrInvalidLength
		}

		open, _ := strconv.ParseFloat(val[1].(string), 64)
		high, _ := strconv.ParseFloat(val[2].(string), 64)
		low, _ := strconv.ParseFloat(val[3].(string), 64)
		closeVal, _ := strconv.ParseFloat(val[4].(string), 64)
		volume, _ := strconv.ParseFloat(val[5].(string), 64)

		result[idx] = entities.Candle{
			OpenTime: int64(val[0].(float64)),
			Open:     open,
			High:     high,
			Low:      low,
			Close:    closeVal,
			Volume:   volume,
		}
	}

	return result, nil
}
