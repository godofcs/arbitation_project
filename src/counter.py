N = 201
BIT_TO_RUB = 2023536.96
INF = 100000000

_fiat = {"RUB", "USD", "EUR", "CNY", "GBP"}
_crypto = {"USDT": 1, "BTC": 2, "BUSD": 3, "BNB": 4, "ETH": 5, "SHIB": 6}
_deC = {1: "USDT", 2: "BTC", 3: "BUSD", 4: "BNB", 5: "ETH", 6: "SHIB"}
_market = {"binance": 1, "bybit": 2, "huobi": 3}
_deM = {1: "binance", 2: "bybit", 3: "huobi"}


def PosByCoin(coin):
    return _crypto[coin.recive_coin] * 10 + _market[coin.market]


def exchange(coin):
    if coin.recive_name.upper() in _fiat:
        return 1
    return coin.price * BIT_TO_RUB


def commission(coin):
    # TODO
    return 0


def PriceByCoin(coin):
    return max(coin.price * (1 - coin.taker_commission), coin.price * (1 - coin.maker_commission)) * exchange \
        (coin) - commission(coin)


def Counter(data: list):
    fiat = []
    crypto = []
    for coins in data:
        if coins.receive_name.upper() in _fiat:
            fiat.append(coins)
        else:
            crypto.append(coins)
    gr = [[] for i in range(N)]
    for toCrypto in crypto:
        pos_of_node = PosByCoin(toCrypto)
        pos_of_root = 0
        if not toCrypto.init_name.upper() in _fiat:
            pos_of_root = _crypto[toCrypto.recive_coin] * 10 + _market[toCrypto.market]
        is_maker = toCrypto.maker_commision != 1
        gr[pos_of_root].append([pos_of_node, PriceByCoin(toCrypto), is_maker])
    for toFiat in fiat:
        pos_of_node = PosByCoin(toFiat)
        is_maker = toFiat.taker_commision != 1  # было maker_comission
        gr[pos_of_node].append([N - 1, PriceByCoin(toFiat), is_maker])
    d = [INF for i in range(N)]
    p = [-1 for i in range(N)]
    p_m = [0 for i in range(N)]
    p[0] = -1
    d[0] = 0

    def dfs(v: int, pred=-1):
        for u in gr[v]:
            d[u[0]] = max(d[u[0]], d[v] + d[u[1]])
            if d[u[0]] < d[v] + u[1]:
                p[u[0]] = v
                p_m[u[0]] = d[u[2]]
            dfs(d[u[0]], v)

    dfs(0)
    pos = N
    ans = ["RUB"]
    while p[pos] != -1:
        pos = p[pos]
        ans.append("->")
        ans.append(_deC[pos/10])
        ans.append(_deM[pos%10])
        if p_m[pos]:
            ans.append("MAKER")
        else:
            ans.append("TAKER")
        ans.append("|")
    ans.append("RUB")
    # return ans
    for i in ans:
        print(i, end=" ")
    return
