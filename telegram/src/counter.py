from src.db_requests.offers import Offer


def Counter(data: list):
    """
    Поиск релазиован с помощью алгоритма поиска наибольшего пути
    в ациклическом графе. Для этого нам нужно транспонировать исходный граф,
    а потом, с помощью методом динамического программирования, найти наиболее
    большой путь. Мы не будем явно транспонировать граф, мы изначально его зададим
    в транспонированном виде.
    """

    N = 71
    INF = 100000000

    _fiat = {"RUB", "USD", "EUR", "CNY", "GBP"}
    _crypto = {"USDT": 1, "BTC": 2, "BUSD": 3, "BNB": 4, "ETH": 5}
    _market = {"binance": 1, "bybit": 2, "huobi": 3}
    _deC = {1: "USDT", 2: "BTC", 3: "BUSD", 4: "BNB", 5: "ETH"}
    _deM = {1: "binance", 2: "bybit", 3: "huobi"}

    class Coin:
        def __init__(self, type, name : str):
            self.type_of_coin = type
            self.name = name

    class LiteOffer:
        """
        Оффер, подобный классу Offer.py, являющийся сжатой его версией.
        Нужен для того, чтобы нормально инициализировать офферы в нашем графе.
        """

        def __init__(self, big_offer):
            self.receive_coin = str(big_offer.receive_coin)
            self.init_coin = str(big_offer.init_coin)
            self.market = big_offer.market
            self.payment = big_offer.payment
            self.sell_buy = big_offer.sell_buy
            self.price = big_offer.price
            self.maker_commission = big_offer.maker_commission
            self.taker_commission = big_offer.taker_commission

        def PosByOffer(self, type_of_offer):
            offer_name = str(self.receive_coin) if type_of_offer == "receive" else str(self.init_coin)
            if offer_name.upper() in _fiat:
                return N - 1 if type_of_offer == "init" else 0
            return _crypto[offer_name] * 10 + _market[self.market]

    def Commission(offer_name):
        # комса указана в рублях
        if offer_name == "BTC":
            return 246.19
        elif offer_name == "USDT":
            return 1.0
        else:
            return 0

    if len(data) == 0:
        return "Invalid input"

    gr = [[] for i in range(N)]
    for offer in data:
        edge_offer = LiteOffer(offer)
        pos_to = edge_offer.PosByOffer("receive")
        if edge_offer.receive_coin.upper() in _fiat:
            gr[0].append(edge_offer) if edge_offer.sell_buy else gr[pos_to].append(edge_offer)
        elif edge_offer.receive_coin in _crypto.keys():
            gr[pos_to].append(edge_offer) if edge_offer.sell_buy else gr[0].append(edge_offer)
        else:
            print(edge_offer.init_coin, edge_offer.receive_coin, edge_offer.market, "<-INVALID COIN",
                  offer.id)
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
    prev = [LiteOffer(Offer()) for i in range(N)]
    dp = [-INF for i in range(N)]
    dp[0] = 0

    def dfs(v: int, p: int):
        for u in gr[v]:
            pos = u.PosByOffer("init")
            cur_commission = (min(u.taker_commission, u.maker_commission)) / 100
            if u.receive_coin in _crypto.keys():
                if dp[pos] == -INF or dp[v] + u.price < dp[pos]:
                    dp[pos] = dp[v] + u.price - u.price * cur_commission
                    prev[pos] = LiteOffer(u)
                    # if pos == N-1:
                    #     print(u.receive_coin, u.init_coin, "in dfs")
                    if pos // 10 == v // 10:
                        print("im here")
                        prev[pos].market = _deM[v % 10] + ","+_deM[pos%10]
            else:
                if u.price - dp[v] > dp[pos]:
                    dp[pos] = u.price - dp[v] - u.price * cur_commission
                    prev[pos] = LiteOffer(u)
                    # if pos == N-1:
                    #     print(u.receive_coin, u.init_coin, "in dfs")

            if p // 10 != v // 10 or v // 10 != pos // 10:
                dfs(pos, v)

    dfs(0, -1)
    ans = str()
    pos = N - 1
    step = 0
    print("____________")
    while pos != 0 and step < 4:
        step += 1
        cur_offer = prev[pos]
        if cur_offer.init_coin != cur_offer.receive_coin:
            ans += "Buy " if cur_offer.sell_buy else "Sell "
            ans += "Taker " if cur_offer.maker_commission > cur_offer.taker_commission else "Maker "
            ans += cur_offer.market + " " + cur_offer.init_coin + " " + cur_offer.receive_coin + " "
            ans += cur_offer.payment + " -> "
        else:
            print(cur_offer.init_coin, cur_offer.receive_coin, cur_offer.market, pos)
            ans += cur_offer.init_coin + " Transfer to next market -> "
        pos = cur_offer.PosByOffer("receive")
    if dp[N - 1] >= 0:
        ans += "PROFITABLY!"
    else:
        ans += "UNPROFITABLY :("
    return ans
