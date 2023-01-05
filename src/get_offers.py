from src.db_requests import db_session
from src.db_requests.offers import Offer


def get_offers(cur_fiat, cur_cripto, cur_limit_id, cur_market, cur_payment):
    sessions = db_session.create_session()
    # TODO Доделать ещё одну, fiat, cripto, receive, init
    offers = sessions.query(Offer).filter(Offer.market == args[0],
                                          Offer.init_coin == args[1],
                                          Offer.receive_coin == args[2],
                                          Offer.payment == args[3],
                                          Offer.id_limit == cur_limit_id).all()
    ans = []
    for offer in offers:
        ans.append(offer)
    return ans
