import ccxt, time

binance = ccxt.binance()

last_prices_list = []
total_profit_pct = []

def calculate_rsi(prices, period):
    if len(prices) <= period:
        raise ValueError("Not enough prices to calculate RSI for the given period")

    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [delta if delta > 0 else 0 for delta in deltas]
    losses = [-delta if delta < 0 else 0 for delta in deltas]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    rsi_values = [100 - (100 / (1 + avg_gain / avg_loss))]

    for i in range(period, len(prices) - 1):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        rsi = 100 - (100 / (1 + avg_gain / avg_loss))
        rsi_values.append(rsi)

    return rsi_values

while True:

    ticker = binance.fetchTicker('BTC/USDT')
    last_price = ticker['last']
    last_prices_list.append(last_price)

    rsi_values_list = calculate_rsi(last_prices_list,5)
    rsi_value = rsi_values_list[len(rsi_values_list)-1]

    profit_pct = (((last_price/entered_price)-1)*100)-0.1

    buy_condition = rsi_value >= 1

    take_profit_condition = profit_pct >= 1
    stop_loss_condition = profit_pct <= -0.5

    if buy_condition:
        buy_order = binance.createMarketBuyOrder('BTC/USDT',1)
        entered_price = buy_order['average']

    if take_profit_condition or stop_loss_condition:
        exit_order = binance.createMarketSellOrder('BTC/USDT',1)
        profit_pct = (((exit_order['average']/entered_price)-1)*100)-0.1
        total_profit_pct.append(profit_pct)

    time.sleep(10)