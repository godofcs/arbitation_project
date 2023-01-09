def get_average_price(glass):
    key = "price"
    summ = 0
    kol = 0
    for pos in glass:
        if pos[key]:
            summ += pos[key]
            kol += 1
    if kol == 0:
        return -1
    return summ / kol


def get_average_ord(glass):
    ord = "col_orders"
    summ = 0
    kol = 0
    for pos in glass:
        if pos[ord]:
            summ += pos[ord]
            kol += 1
    if kol == 0:
        return 0
    return summ / kol


def analyse_users(glass):
    ord = "col_orders"
    per = "complete_percent"
    average_ord = get_average_ord(glass)
    trust_users = []
    for pos in glass:
        if pos[ord] > min(average_ord, 900) and pos[per] > 95.0:
            trust_users.append((pos))
    return trust_users


def analyse_glass(glass):
    reliable_users = analyse_users(glass)
    average_price = get_average_price(reliable_users)
    #print(average_price)
    return average_price
