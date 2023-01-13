from src.db_requests import db_session
from src.db_requests.offers import Offer


limits = {1: 1000, 2: 5000, 3: 10000, 4: 25000, 5: 50000, 6: 100000}


# Эта функция отвечает за выбор нужных пользователю офферов
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
                        offers = sessions.query(Offer).filter(Offer.market == it_market,
                                                              Offer.init_coin == it_fiat,
                                                              Offer.receive_coin == it_crypto,
                                                              Offer.payment == it_payment,
                                                              Offer.id_limit == it_limit_id).all()
                        rev_offers = sessions.query(Offer).filter(Offer.market == it_market,
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
