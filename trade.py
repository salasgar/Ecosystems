from random import *
from copy import *
from Basic_tools import *


def default_minimum_reserve_value_after_mutation(minimum_reserve):
    # Decide the number of data that will change:
    number_of_changes = randint(0, 1 + len(minimum_reserve)/4)
    # Do the changes:
    for i in range(number_of_changes):
        product = randint(0, len(minimum_reserve) - 1)
        new_value = gauss(
            minimum_reserve[product],
            0.0001 + minimum_reserve[product] * 0.01
            )
        minimum_reserve[product] = max(0, new_value)
    return minimum_reserve


def default_matrix_of_prices_value_after_mutation(matrix_of_prices):
    size_x, size_y = len(matrix_of_prices), len(matrix_of_prices[0])
    # Decide the number of data that will change:
    number_of_changes = randint(0, 1 + size_x * size_y / 8)
    # Do the changes:
    for i in range(number_of_changes):
        product_for_sale = randint(0, size_x - 1)
        product_to_buy_with = randint(0, size_y - 1)
        new_value = gauss(
            matrix_of_prices[product_for_sale][product_to_buy_with],
            0.0001 + matrix_of_prices[
                product_for_sale][product_to_buy_with] * 0.01
            )
        matrix_of_prices[product_for_sale][
            product_to_buy_with] = max(0, new_value)
    return matrix_of_prices


class Stock_market:
    def __init__(self, *product_names):
        self.list_of_product_names = product_names
        self.product_code = {
            name: product_names.index(name)
            for name in product_names
            }
        self.number_of_products = len(product_names)
        self.list_of_brokers = []

    def add_new_broker(self, new_broker):
        self.list_of_brokers.append(new_broker)

    def delete_broker(self, broker):
        del self.list_of_brokers[self.list_of_brokers.index(broker)]


class Broker:
    def __init__(self, parent_stock_market, parent_broker=None):
        self.parent_stock_market = parent_stock_market
        self.number_of_products = parent_stock_market.number_of_products
        if parent_broker is None:
            self.reserve = [
                random()
                for product in range(self.number_of_products)
            ]
            self.minimum_reserve = [
                random()
                for product in range(self.number_of_products)
            ]
            self.matrix_of_prices = [
                [
                    random()*2
                    for product_to_buy_with in range(self.number_of_products)
                ]
                for product_for_sale in range(self.number_of_products)
            ]
            self.minimum_reserve_value_after_mutation = \
                default_minimum_reserve_value_after_mutation
            self.matrix_of_prices_value_after_mutation = \
                default_matrix_of_prices_value_after_mutation
        else:
            self.reserve = deepcopy(parent_broker.reserve)
            self.minimum_reserve_value_after_mutation = \
                parent_broker.minimum_reserve_value_after_mutation
            self.matrix_of_prices_value_after_mutation = \
                parent_broker.matrix_of_prices_value_after_mutation
            self.minimum_reserve = self.minimum_reserve_value_after_mutation(
                deepcopy(parent_broker.minimum_reserve)
                )
            self.matrix_of_prices = self.matrix_of_prices_value_after_mutation(
                deepcopy(parent_broker.matrix_of_prices)
                )

    def amount_for_sale(self, product_code):
        return max(
            0,
            self.reserve[product_code] - self.minimum_reserve[product_code]
        )

    def price(self, product_for_sale, product_to_buy_with):
        return self.matrix_of_prices[product_for_sale][product_to_buy_with]

    def set_mutation_method_of_minimum_reserve(self, mutation_method):
        self.minimum_reserve_value_after_mutation = mutation_method

    def set_mutation_method_of_matrix_of_prices(self, mutation_method):
        self.matrix_of_prices_value_after_mutation = mutation_method

    def mutate(self):
        self.minimum_reserve = self.minimum_reserve_value_after_mutation(
            self.minimum_reserve
            )
        self.matrix_of_prices = self.matrix_of_prices_value_after_mutation(
            self.matrix_of_prices
            )

    def find_matching_trade_offers(self, seller):
        matching_offers_list = []
        for product_for_sale in range(self.number_of_products):
            if seller.amount_for_sale(product_for_sale) > 0:
                for product_to_buy_with in range(self.number_of_products):
                    if (
                        product_for_sale != product_to_buy_with
                        and
                        self.amount_for_sale(product_to_buy_with) > 0
                        and
                        self.matrix_of_prices[
                            product_to_buy_with][product_for_sale] > 0
                        and
                        seller.matrix_of_prices[
                            product_for_sale][product_to_buy_with]
                        <
                        1.0 / self.matrix_of_prices[
                            product_to_buy_with][product_for_sale]
                            ):
                        price = seller.matrix_of_prices[
                            product_for_sale][product_to_buy_with]
                        if price > 0:
                            amount = min(
                                seller.amount_for_sale(product_for_sale),
                                self.amount_for_sale(
                                    product_to_buy_with
                                ) / price
                            )
                            matching_offer = (
                                product_for_sale,
                                product_to_buy_with,
                                amount
                            )
                            matching_offers_list.append(matching_offer)
        return matching_offers_list


""" TESTING CLASS Stock_market """


def print_statistics():
    print ' *** STATISTICS: *** '
    print 'time:', time,
    N_of_brokers = len(stock_market.list_of_brokers)
    print 'brokers:', N_of_brokers, 'average prices:'
    matrix_of_average_prices = [
        [0 for j in range(N_of_products)]
        for i in range(N_of_products)
    ]
    for broker in stock_market.list_of_brokers:
        for i in range(N_of_products):
            for j in range(N_of_products):
                matrix_of_average_prices[i][j] += broker.matrix_of_prices[i][j]
    for i in range(N_of_products):
        for j in range(N_of_products):
            matrix_of_average_prices[i][j] /= float(N_of_brokers)
    for i in range(N_of_products):
        print [round(item, 3) for item in matrix_of_average_prices[i]]


def is_dead_after_subtracting_costs(broker):
    for n in range(broker.number_of_products):
        broker.reserve[n] -= random() * costs[n]
        if broker.reserve[n] < 0:
            return True
    return False


Number_of_actors_who_find_products_each_cycle = 200
Number_of_actors_who_reproduce_themselves_each_cycle = 100
Number_of_actors_who_will_trade = 200

stock_market = Stock_market('gold', 'silver', 'iron', 'plumb', 'platinum')
# Number of units of each product that every broker has to spend each cycle:
costs = [0.1, 0.2, 0.4, 0.8, 1.6]
N_of_products = len(costs)

for _ in range(300):
    new_broker = Broker(stock_market)
    stock_market.add_new_broker(new_broker)

Time_to_end = 10000

time = 0

while time < Time_to_end:
    # PRODUCTION:
    for broker in sample(
        stock_market.list_of_brokers,
        min(
            len(stock_market.list_of_brokers),
            Number_of_actors_who_find_products_each_cycle
        )
            ):
        for n in range(stock_market.number_of_products):
            broker.reserve[n] += random()

    # REPRODUCTION:
    for parent_broker in sample(
        stock_market.list_of_brokers,
        min(
            len(stock_market.list_of_brokers),
            Number_of_actors_who_reproduce_themselves_each_cycle
        )
            ):
        new_broker = Broker(stock_market, parent_broker)
        stock_market.add_new_broker(new_broker)

    # TRADE:
    brokers_who_buy = sample(
        stock_market.list_of_brokers,
        min(
            len(stock_market.list_of_brokers),
            Number_of_actors_who_will_trade
        )
    )
    brokers_who_sell = sample(
        stock_market.list_of_brokers,
        min(
            len(stock_market.list_of_brokers),
            Number_of_actors_who_will_trade
        )
    )
    couples_for_trade = zip(brokers_who_sell, brokers_who_buy)
    for (seller, buyer) in couples_for_trade:
        if seller != buyer:
            matching_offers_list = buyer.find_matching_trade_offers(seller)
            if len(matching_offers_list) > 0:
                (
                    product_for_sale,
                    product_to_buy_with,
                    amount
                ) = choice(matching_offers_list)

                price = seller.price(
                    product_for_sale,
                    product_to_buy_with)
                amount_of_product_to_buy_with = amount * price

                will_print = random_true(1)
                if will_print:
                    print_statistics()
                    print 'Buyer index:', buyer.matrix_of_prices[
                        1][0] * buyer.matrix_of_prices[0][1]
                    print 'Seller index:', seller.matrix_of_prices[
                        1][0] * seller.matrix_of_prices[0][1]
                    print 'product for sale:', product_for_sale,
                    print 'cost:', costs[product_for_sale],
                    print 'product to buy with:', product_to_buy_with,
                    print 'cost:', costs[product_to_buy_with],
                    print 'amount:', amount,
                    print 'amount to buy with:', amount_of_product_to_buy_with,
                    print 'price:', price
                    print 'Buyer previous reserves:',
                    print product_for_sale, buyer.reserve[product_for_sale],
                    print product_to_buy_with, buyer.reserve[
                        product_to_buy_with],
                    print 'Seller previous reserves:',
                    print product_for_sale, seller.reserve[product_for_sale],
                    print product_to_buy_with, seller.reserve[
                        product_to_buy_with]
                    print 'Buyer prices:'
                    for i in range(N_of_products):
                        print [
                            round(item, 3)
                            for item in buyer.matrix_of_prices[i]
                            ]
                    print 'Seller prices:'
                    for i in range(N_of_products):
                        print [
                            round(item, 3)
                            for item in seller.matrix_of_prices[i]
                            ]

                buyer.reserve[product_for_sale] += amount
                seller.reserve[product_for_sale] -= amount
                buyer.reserve[
                    product_to_buy_with] -= amount_of_product_to_buy_with
                seller.reserve[
                    product_to_buy_with] += amount_of_product_to_buy_with

                if will_print:
                    print 'Buyer reserves:',
                    print product_for_sale, buyer.reserve[product_for_sale],
                    print product_to_buy_with, buyer.reserve[
                        product_to_buy_with],
                    print 'Seller reserves:',
                    print product_for_sale, seller.reserve[product_for_sale],
                    print product_to_buy_with, seller.reserve[
                        product_to_buy_with]

    # COSTS OF LIVING:
    i = 0
    while i < len(stock_market.list_of_brokers):
        broker = stock_market.list_of_brokers[i]
        if is_dead_after_subtracting_costs(broker):
            del stock_market.list_of_brokers[i]
        else:
            i += 1

    if time % 10000 == 0:
        print_statistics()
    time += 1

