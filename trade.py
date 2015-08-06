from random import *
from copy import *


def default_minimum_reserve_value_after_mutation(minimum_reserve):
    n = randint(0, 1 + len(minimum_reserve)/4)
    for i in range(n):
        product = randint(0, len(minimum_reserve) - 1)
        new_value = gauss(
            minimum_reserve[product],
            0.0001 + minimum_reserve[product] * 0.05
            )
        minimum_reserve[product] = max(0, new_value)
    return minimum_reserve


def default_matrix_of_prices_value_after_mutation(matrix_of_prices):
    size_x, size_y = len(matrix_of_prices), len(matrix_of_prices[0])
    n = randint(0, 1 + size_x * size_y / 8)
    for i in range(n):
        product_for_sale = randint(0, size_x - 1)
        product_to_buy_with = randint(0, size_y - 1)
        new_value = gauss(
            matrix_of_prices[product_for_sale][product_to_buy_with],
            0.0001 + matrix_of_prices[
                product_for_sale][product_to_buy_with] * 0.05
            )
        matrix_of_prices[product_for_sale][product_to_buy_with] = new_value
    return matrix_of_prices


class Stock_market:
    def __init__(self, *product_names):
        self.list_of_product_names = product_names
        self.product_code = {
            name: product_names.index(name)
            for name in product_names
            }
        self.n = len(product_names)
        self.list_of_brokers = []

    def add_new_broker(self, new_broker):
        self.list_of_brokers.append(new_broker)


class Broker:
    def __init__(self, parent_stock_market, parent_broker=None):
        self.parent_stock_market = parent_stock_market
        self.n = parent_stock_market.n
        if parent_broker is None:
            self.reserve = [
                random()
                for product in range(self.n)
            ]
            self.minimum_reserve = [
                random()
                for product in range(self.n)
            ]
            self.matrix_of_prices = [
                [
                    random()*2
                    for product_to_buy_with in range(self.n)
                ]
                for product_for_sale in range(self.n)
            ]
            self.minimum_reserve_value_after_mutation = \
                default_minimum_reserve_value_after_mutation
            self.matrix_of_prices_value_after_mutation = \
                default_matrix_of_prices_value_after_mutation
        else:
            self.reserve = copy(parent_broker.reserve)
            self.minimum_reserve = copy(parent_broker.minimum_reserve)
            self.matrix_of_prices = copy(parent_broker.matrix_of_prices)
            self.minimum_reserve_value_after_mutation = \
                parent_broker.minimum_reserve_value_after_mutation
            self.matrix_of_prices_value_after_mutation = \
                parent_broker.matrix_of_prices_value_after_mutation

    def amount_for_sale(self, product_code):
        return max(0, self.reserve[code] - self.minimum_reserve[code])

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
        for product_for_sale in range(self.n):
            if seller.amount_for_sale(product_for_sale) > 0:
                for product_to_buy_with in range(self.n):
                    if (
                        self.amount_for_sale(product_to_buy_with) > 0
                        and
                        seller.matrix_of_prices[
                            product_for_sale][product_to_buy_with]
                        <
                        1.0 / self.matrix_of_prices[
                            product_to_buy_with][product_for_sale]
                            ):
                        price = seller.matrix_of_prices[
                            product_for_sale][product_to_buy_with]
                        amount = min(
                            seller.amount_for_sale(product_for_sale),
                            self.amount_for_sale(product_to_buy_with) / price
                        )
                        matching_offer = (
                            product_for_sale,
                            product_to_buy_with,
                            amount
                        )
                        matching_offers_list.append(matching_offer)
        return matching_offers_list












