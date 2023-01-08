import datetime


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


#glass = [{'name': 'Islam.', 'col_orders': 125, 'complete_percent': 97.0, 'price': 65.05, 'limit': [500.0, 100000.0], 'available': 1352.8}, {'name': 'Evgenio 1', 'col_orders': 171, 'complete_percent': 98.0, 'price': 65.04, 'limit': [1000.0, 30000.0], 'available': 669.0}, {'name': 'Вера С', 'col_orders': 590, 'complete_percent': 99.0, 'price': 65.03, 'limit': [1000.0, 20000.0], 'available': 1116.080243}, {'name': 'davlat28', 'col_orders': 361, 'complete_percent': 96.0, 'price': 65.03, 'limit': [1000.0, 2000000.0], 'available': 430.0}, {'name': 'RUIIIKA', 'col_orders': 99, 'complete_percent': 100.0, 'price': 65.0, 'limit': [1000.0, 52000.0], 'available': 800.0}, {'name': 'kostya547', 'col_orders': 31, 'complete_percent': 100.0, 'price': 64.98, 'limit': [1000.0, 10000.0], 'available': 114.99992}, datetime.datetime(2022, 12, 11, 16, 21, 39, 943689)]
#analyse_glass(glass)