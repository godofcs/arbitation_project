from src.db_requests import db_session
from src.db_requests.offers import Offer


limits = {1: 1000, 2: 5000, 3: 10000, 4: 25000, 5: 50000, 6: 100000}
rev_limits = {1000: 1, 5000: 2, 10000: 3, 25000: 4, 50000: 5, 100000: 6}


def get_limits_list(limit):
    limit = int(limit)
    cur_limit_id = []
    for lim in sorted(rev_limits.keys())[::-1]:
        if limit <= lim:
            cur_limit_id.append(rev_limits[lim])
    kol_iteration = 0
    lim = cur_limit_id[0] - 1
    while kol_iteration < 2 and lim > 0:
        cur_limit_id.append(lim)
        lim -= 1
        kol_iteration += 1
    return cur_limit_id


def get_offers(cur_fiat: list, cur_cripto: list, cur_limit_id: list, cur_market: list, cur_payment: list):
    sessions = db_session.create_session()
    all_offers = []
    for it_limit_id in cur_limit_id:
        ans_for_one_limit_id = [limits[it_limit_id]]
        for it_crypto in cur_cripto:
            ans = []
            for it_payment in cur_payment:
                for it_market in cur_market:
                    for it_fiat in cur_fiat:
                        # TODO проверить, что с .lower(), всё работает
                        offers = sessions.query(Offer).filter(Offer.market == it_market.lower(),
                                                              Offer.init_coin == it_fiat,
                                                              Offer.receive_coin == it_crypto,
                                                              Offer.payment == it_payment,
                                                              Offer.id_limit == it_limit_id).all()
                        rev_offers = sessions.query(Offer).filter(Offer.market == it_market.lower(),
                                                                  Offer.init_coin == it_crypto,
                                                                  Offer.receive_coin == it_fiat,
                                                                  Offer.payment == it_payment,
                                                                  Offer.id_limit == it_limit_id).all()
                        for offer in offers:
                            ans.append(offer)
                        for offer in rev_offers:
                            ans.append(offer)
            ans_for_one_limit_id.append(ans)
        all_offers.append(ans_for_one_limit_id)
    return all_offers
