from src.db_requests.offers import Offer

N = 81
INF = 100000000

_fiat = {"RUB", "USD", "EUR", "CNY", "GBP"}
_crypto = {"USDT": 1, "BTC": 2, "BUSD": 3, "BNB": 4, "ETH": 5, "SHIB": 6}
_market = {"binance": 1, "bybit": 2, "huobi": 3}
_deC = {1: "USDT", 2: "BTC", 3: "BUSD", 4: "BNB", 5: "ETH", 6: "SHIB"}
_deM = {1: "binance", 2: "bybit", 3: "okx"}

class _LiteOffer:
    def __init__(self, init_name, receive_name, market, maker_commission, taker_commission, price, sell_buy):
        self.init_name = init_name
        self.receive_name = receive_name
        self.market = market
        self.maker_commission = maker_commission
        self.taker_commission = taker_commission
        self.price = price
        self.sell_buy = sell_buy


def PosByCoin(coin: _LiteOffer, type_of_coin: str):
    coin_name = coin.receive_name if type_of_coin == "receive" else coin.init_name
    if coin_name.upper() in _fiat:
        return N - 1 if type_of_coin == "init" else 0
    return _crypto[coin_name] * 10 + _market[coin.market]


def Commission(coin_name):
    # комса указана в рублях
    if coin_name == "BTC":
        return 246.19
    elif coin_name == "ETH":
        return 10.0
    elif coin_name == "USDT":
        return 80.0
    elif coin_name == "BUSD":
        return 0
    elif coin_name == "BNB":
        return 0
    elif coin_name == "SHIB":
        return 0
    else:
        # TODO добавить лог, что пригшла невалидная монета
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
        lite_offer = _LiteOffer(offer.init_coin, offer.receive_coin, offer.market,
                                offer.maker_commission, offer.taker_commission, offer.price, offer.sell_buy)
        if offer.receive_name.upper() in _fiat:
            gr[0].append(lite_offer)
        elif offer.receive_name in _crypto.keys():
            gr[PosByCoin(offer, "receive")].append(lite_offer)
        # TODO Вот тут можно прикрутить лог, если пришла непонятная моментка
    for i in range(1, 7):
        for j in range(1, 4):
            for k in range(j):
                gr[i * 10 + j].append(_LiteOffer(_deC[i], _deC[i], _deM[k], 0, 0, Commission(_deC[i]), None))
                # здесь в поле маркет указано, куда мы переводим монеты
    prev = [_LiteOffer(data[0]) for i in range(N)] # возможен out_of_range
    prev[0] = -1
    dp = [-INF for i in range(N)]
    dp[0] = 0

    def dfs(v: int, p: int):
        for u in gr[v]:
            pos = PosByCoin(u, "init")
            if dp[v] + u.price > dp[pos]:
                dp[pos] = dp[v] + u.price
                prev[pos] = u
            if p // 10 != v // 10:
                dfs(pos, v)

    dfs(0, -1)
    ans = str()
    pos = N - 1
    while pos != 0:
        cur_offer = prev[pos]
        # TODO Добавить справку о обозначениях в Хелп
        if cur_offer.init_name != cur_offer.receive_name:
            ans += "Buy " if cur_offer.sell_buy else "Sell "
            ans += "Taker " if cur_offer.maker_commission == 100 else "Maker "
            ans += cur_offer.market + " " + cur_offer.init_name + " " + cur_offer.receive_name + " | "
        else:
            ans += cur_offer.init_name + " Transfer to next market | "
        pos = PosByCoin(cur_offer, "receive")
    return ans
