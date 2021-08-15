def get_user_query():
    user_query = input("Write action (buy, fill, take, remaining, exit):\n")
    return user_query


def get_coffee_type():
    coffee_type = input("""What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, \
    back - to main menu:\n""")
    return coffee_type


# Stage 6/6
class CoffeeMachine:
    n = 0

    def __new__(cls, *args, **kwargs):
        if cls.n == 0:
            cls.n += 1
            return object.__new__(cls)

    def __init__(self, supplies_stock, money, coffee_receipts):
        self.supplies_stock = supplies_stock
        self.money = money
        self.coffee_receipts = coffee_receipts
        self.missing_supply = []

    def __repr__(self):
        return ""

    def __str__(self):
        return ""

    def get_supplies_stock(self):
        return self.supplies_stock

    def get_money_stock(self):
        return self.money

    def print_coffee_machine_state(self):
        print(f"""The coffee machine has:
        \r{self.supplies_stock['Water']} of water
        \r{self.supplies_stock['Milk']} of milk
        \r{self.supplies_stock['Coffee Beans']} of coffee beans
        \r{self.supplies_stock['Disposable Cups']} of disposable cups
        \r{self.money} of money""")

    def withdraw_money(self):
        print(f"I gave you ${self.money}")
        self.money = 0

    def fill_coffee_machine(self, supplies):
        self.supplies_stock['Water'] += supplies['Water']
        self.supplies_stock['Milk'] += supplies['Milk']
        self.supplies_stock['Coffee Beans'] += supplies['Coffee Beans']
        self.supplies_stock['Disposable Cups'] += supplies['Disposable Cups']

    def add_money(self, money):
        self.money += money

    def missing_supplies(self, coffee_receipt):
        missing_supply = []
        if self.supplies_stock['Water'] < coffee_receipt['Water']:
            missing_supply.append('water')
        if self.supplies_stock['Milk'] < coffee_receipt['Milk']:
            missing_supply.append('milk')
        if self.supplies_stock['Coffee Beans'] < coffee_receipt['Coffee Beans']:
            missing_supply.append('coffee beans')
        if self.supplies_stock['Disposable Cups'] < 1:
            missing_supply.append('disposable cups')
        return missing_supply

    def prepare_coffee(self, coffee_type):
        coffee_receipt = {}
        if coffee_type == '1':
            coffee_receipt = self.coffee_receipts['Espresso']
        elif coffee_type == '2':
            coffee_receipt = self.coffee_receipts['Latte']
        elif coffee_type == '3':
            coffee_receipt = self.coffee_receipts['Cappuccino']

        missing_supply = self.missing_supplies(coffee_receipt)
        if any(missing_supply):
            for supply in missing_supply:
                print(f"Sorry, not enough {supply}")
            self.money = 0
        else:
            print("I have enough resources, making you a coffee!")
            self.supplies_stock['Water'] -= coffee_receipt['Water']
            self.supplies_stock['Milk'] -= coffee_receipt['Milk']
            self.supplies_stock['Coffee Beans'] -= coffee_receipt['Coffee Beans']
            self.supplies_stock['Disposable Cups'] -= 1
            self.money += coffee_receipt['Cost']


def main():
    money = 550

    supplies_stock = {'Water': 400,  # ml
                      'Milk': 540,  # ml
                      'Coffee Beans': 120,  # g
                      'Disposable Cups': 9}

    coffee_receipts = {'Espresso':   {'Water': 250,           # ml
                                      'Milk': 0,              # ml
                                      'Coffee Beans': 16,     # g
                                      'Cost': 4},             # $
                       'Latte':      {'Water': 350,           # ml
                                      'Milk': 75,             # ml
                                      'Coffee Beans': 20,     # g
                                      'Cost': 7},             # $
                       'Cappuccino': {'Water': 200,           # ml
                                      'Milk': 100,            # ml
                                      'Coffee Beans': 12,     # g
                                      'Cost': 6}}             # $

    coffee_machine = CoffeeMachine(supplies_stock, money, coffee_receipts)

    while True:
        user_query = get_user_query()
        if user_query == "exit":
            break
        elif user_query == "remaining":
            coffee_machine.print_coffee_machine_state()
        elif user_query == "buy":
            coffee_type = get_coffee_type()
            if coffee_type == "back":
                continue
            coffee_machine.prepare_coffee(coffee_type)
        elif user_query == "fill":
            supplies = {'Water': abs(int(input("Write how many ml of water you want to add:\n"))),
                        'Milk': abs(int(input("Write how many ml of milk you want to add:\n"))),
                        'Coffee Beans': abs(int(input("Write how many grams of coffee beans you want to add:\n"))),
                        'Disposable Cups': abs(int(input("Write how many disposable coffee cups you want to add:\n")))}
            coffee_machine.fill_coffee_machine(supplies)
        elif user_query == "take":
            coffee_machine.withdraw_money()


if __name__ == '__main__':
    main()
