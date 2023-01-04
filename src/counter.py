from src.db_requests.offers import Offer

N = 201
INF = 100000000

_fiat = {"RUB", "USD", "EUR", "CNY", "GBP"}
_crypto = {"USDT": 1, "BTC": 2, "BUSD": 3, "BNB": 4, "ETH": 5, "SHIB": 6}
_market = {"binance": 1, "bybit": 2, "huobi": 3}


def PosByCoin(coin: Offer, type_of_coin: str):
    coin_name = coin.recive_coin if type_of_coin == "receive" else coin.init_coin
    if coin_name.upper() in _fiat:
        return N - 1
    return _crypto[coin_name] * 10 + _market[coin.market]


def Commission(coin):
    # TODO
    return 0


def Counter(data: list):
    """
    Поиск релазиован с помощью алгоритма поиска наибольшего пути
    в ациклическом графе. Для этого нам нужно транспонировать исходный граф,
    а потом, с помощью методом динамического программирования, найти наиболее
    большой путь. Мы не будем явно транспонировать граф, мы изначально его зададим
    в транспонированном виде.
    """
    gr = [[] for i in range(N)]
    for offer in data:
        if offer.receive_coin.upper() in _fiat:
            gr[0].append(offer)
        elif offer.receive_coin in _crypto.keys():
            gr[PosByCoin(offer, "init")].append(offer)
        # TODO Вот тут можно прикрутить лог, если пришла непонятная моментка
    prev = [data[0] for i in range(N)]
    prev[0] = -1
    dp = [-INF for i in range(N)]
    dp[0] = 0

    def dfs(v: int):
        for u in gr[v]:
            pos = PosByCoin(u, "init")
            if dp[v] + u.price > dp[pos]:
                dp[pos] = dp[v] + u.price
                prev[pos] = u

    dfs(0)
    ans = str()
    pos = N - 1
    while pos != -1:
        cur_offer = prev[pos]
        # TODO Добавить справку о обозначениях в Хелп
        ans += "Buy" if cur_offer.sell_buy else "Sell"
        ans += "Taker" if cur_offer.maker_commission == 100 else "Maker"
        ans += cur_offer.market + cur_offer.init_coin + cur_offer.recieve_coin + " -> "
        pos = PosByCoin(cur_offer, "receive")
    return ans
