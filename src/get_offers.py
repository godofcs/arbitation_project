from src.db_requests import db_session
from src.db_requests.offers import Offer


def get_offers(cur_fiat: list, cur_cripto: list, cur_limit_id: list, cur_market: list, cur_payment: list):
    sessions = db_session.create_session()
    all_offers = []
    for crypto in cur_cripto:
        ans = []
        for payment in cur_payment:
            for limit_id in cur_limit_id:
                for market in cur_market:
                    for fiat in cur_fiat:
                        offers = sessions.query(Offer).filter(Offer.market == market,
                                                              Offer.init_coin == fiat,
                                                              Offer.receive_coin == crypto,
                                                              Offer.payment == payment,
                                                              Offer.id_limit == limit_id).all()
                        rev_offers = sessions.query(Offer).filter(Offer.market == market,
                                                                  Offer.init_coin == crypto,
                                                                  Offer.receive_coin == fiat,
                                                                  Offer.payment == payment,
                                                                  Offer.id_limit == limit_id).all()
                        for offer in offers:
                            ans.append(offer)
                        for offer in rev_offers:
                            ans.append(offer)
        all_offers.append(ans)
    return all_offers
