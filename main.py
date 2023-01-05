from src.parsers import parse_argument as pa
from src import get_offers as go
from src import counter


if __name__ == "__main__":
    #limit_id, fiat_mas, market_mas, crypto_mas, payment_mas = get_next_position_in_query()
    ans = go.get_offers()
    print(ans)
    print(counter.Counter(ans))



