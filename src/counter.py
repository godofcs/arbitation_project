from src.db_requests.offers import Offer


def Counter(data: list):
    N = 71
    INF = 100000000

    class LiteOffer:
        def __init__(self, big_offer):
            self.receive_coin = big_offer.receive_coin
            self.init_coin = big_offer.init_coin
            self.market = big_offer.market
            self.payment = big_offer.payment
            self.sell_buy = big_offer.sell_buy
            self.price = float(big_offer.price)
            self.maker_commission = big_offer.maker_commission
            self.taker_commission = big_offer.taker_commission

    _fiat = {"RUB", "USD", "EUR", "CNY", "GBP"}
    _crypto = {"USDT": 1, "BTC": 2, "BUSD": 3, "BNB": 4, "ETH": 5}
    _market = {"binance": 1, "bybit": 2, "huobi": 3}
    _deC = {1: "USDT", 2: "BTC", 3: "BUSD", 4: "BNB", 5: "ETH"}
    _deM = {1: "binance", 2: "bybit", 3: "huobi"}

    def PosByOffer(offer: LiteOffer, type_of_offer: str):
        offer_name = offer.receive_coin if type_of_offer == "receive" else offer.init_coin
        if offer_name.upper() in _fiat:
            return N - 1 if type_of_offer == "init" else 0
        return _crypto[offer_name] * 10 + _market[offer.market]

    def Commission(offer_name):
        # комса указана в рублях
        if offer_name == "BTC":
            return 246.19
        elif offer_name == "USDT":
            return 1.0
        else:
            return 0

    """
    Поиск релазиован с помощью алгоритма поиска наибольшего пути
    в ациклическом графе. Для этого нам нужно транспонировать исходный граф,
    а потом, с помощью методом динамического программирования, найти наиболее
    большой путь. Мы не будем явно транспонировать граф, мы изначально его зададим
    в транспонированном виде.
    """
    if len(data) == 0:
        return "Invalid input"
    gr = [[] for i in range(N)]
    for offer in data:
        lite_offer = LiteOffer(offer)
        if lite_offer.receive_coin.upper() in _fiat:
            gr[0].append(lite_offer)
        elif lite_offer.receive_coin in _crypto.keys():
            gr[PosByOffer(lite_offer, "receive")].append(lite_offer)
        # TODO Вот тут можно прикрутить лог, если пришла непонятная моментка
    for i in range(1, len(_crypto) + 1):
        for j in range(2, len(_market) + 1):
            for k in range(1, j):
                modificate_offer = LiteOffer(data[0])
                modificate_offer.init_coin, modificate_offer.receive_coin, modificate_offer.price, modificate_offer.market = \
                    _deC[i], _deC[i], Commission(_deC[i]), _deM[k]
                offer_between_markets_1 = LiteOffer(modificate_offer)
                gr[i * 10 + j].append(offer_between_markets_1)
                modificate_offer.market = _deM[j]
                offer_between_markets_2 = LiteOffer(modificate_offer)
                gr[i * 10 + k].append(offer_between_markets_2)
                # здесь в поле маркет указано, куда мы переводим монеты
    prev = [None for i in range(N)]
    dp = [-INF for i in range(N)]
    dp[0] = 0

    def dfs(v: int, p: int):
        for u in gr[v]:
            pos = PosByOffer(u, "init")
            cur_commission = (u.taker_commission if u.maker_commission == 100 else u.maker_commission) / 100
            if u.receive_coin in _crypto.keys():
                if dp[pos] == -INF:
                    dp[pos] = dp[v] + u.price - u.price * cur_commission
                    prev[pos] = u
                elif dp[v] + u.price < dp[pos]:
                    dp[pos] = dp[v] + u.price - u.price * cur_commission
                    prev[pos] = u
                    if p // 10 == v // 10:
                        prev[pos].market = _deM[p % 10]
            else:
                if u.price - dp[v] > dp[pos]:
                    dp[pos] = u.price - dp[v] - u.price * cur_commission
                    prev[pos] = u

            if p // 10 != v // 10 or v // 10 != pos // 10:
                dfs(pos, v)

    dfs(0, -1)
    ans = str()
    pos = N - 1
    while pos != 0:
        cur_offer = prev[pos]
        if cur_offer.init_coin != cur_offer.receive_coin:
            ans += "Buy " if cur_offer.sell_buy else "Sell "
            ans += "Taker " if cur_offer.maker_commission == 100 else "Maker "
            ans += cur_offer.market + " " + cur_offer.init_coin + " " + cur_offer.receive_coin + " "
            ans += cur_offer.payment + " -> "
        else:
            ans += cur_offer.init_coin + " Transfer to next market -> "
        pos = PosByOffer(cur_offer, "receive")
    if dp[N - 1] >= 0:
        ans += "PROFITABLY!"
    else:
        ans += "UNPROFITABLY :("
    return ans
