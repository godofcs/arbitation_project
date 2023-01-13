def get_average_price(glass):  # Эта функция считает среднее значение цены в стакане
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


def get_average_ord(glass):  # Эта функция считает среднее количество ордеров у тейкеров в стакане
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


def analyse_users(glass):  # Эта функция отсеивает ненадёжных мейкеров
    ord = "col_orders"
    per = "complete_percent"
    average_ord = get_average_ord(glass)
    trust_users = []
    for pos in glass:
        if pos[ord] > average_ord and pos[per] > 95.0:
            trust_users.append((pos))
    return trust_users


def analyse_glass(glass):  # Эта функция отвечает за запуск анализа стакана
    reliable_users = analyse_users(glass)
    average_price = get_average_price(reliable_users)
    return average_price
