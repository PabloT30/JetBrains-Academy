import math
import argparse


def calculate_periods(args):
    loan_principal = args.principal
    annuity = args.payment
    loan_interest = args.interest

    nominal_loan_interest = loan_interest / (12 * 100)

    number_of_months = math.log(annuity / (annuity - nominal_loan_interest * loan_principal),
                                1 + nominal_loan_interest)

    if number_of_months < 12:
        print(f"It will take {round(number_of_months)} "
              f"{'month' if number_of_months == 1 else 'months'} "
              f"to repay this loan!")
        number_of_months = round(number_of_months)
    elif number_of_months % 12 > 11:
        number_of_years = number_of_months // 12 + 1
        print(f"It will take {round(number_of_years)} "
              f"{'year' if number_of_years == 1 else 'years'} to repay this loan!")
        number_of_months = round(number_of_years) * 12
    elif number_of_months % 12 == 0:
        number_of_years = number_of_months // 12
        print(f"It will take {round(number_of_years)} "
              f"{'year' if number_of_years == 1 else 'years'} to repay this loan!")
        number_of_months = round(number_of_years) * 12
    else:
        number_of_years = number_of_months // 12
        print(f"It will take {round(number_of_years)} "
              f"{'year' if number_of_years == 1 else 'years'} "
              f"and {math.ceil(number_of_months % 12)} "
              f"{'month' if number_of_months % 12 == 1 else 'months'} "
              f"to repay this loan!")
        number_of_months = round(number_of_years) * 12 + math.ceil(number_of_months % 12)

    return loan_principal, annuity, number_of_months


def calculate_payment(args):
    loan_principal = args.principal
    number_of_months = args.periods
    loan_interest = args.interest

    nominal_loan_interest = loan_interest / (12 * 100)

    annuity = loan_principal * ((nominal_loan_interest
                                 * math.pow(1 + nominal_loan_interest, number_of_months))
                                / (math.pow(1 + nominal_loan_interest, number_of_months) - 1))

    annuity = math.ceil(annuity)
    print(f"Your monthly payment = {annuity}!")
    return loan_principal, annuity, number_of_months


def calculate_principal(args):
    annuity = args.payment
    number_of_months = args.periods
    loan_interest = args.interest

    nominal_loan_interest = loan_interest / (12 * 100)

    loan_principal = annuity / ((nominal_loan_interest * math.pow(1 + nominal_loan_interest, number_of_months))
                                / (math.pow(1 + nominal_loan_interest, number_of_months) - 1))

    loan_principal = round(loan_principal)
    print(f"Your loan principal = {loan_principal}!")
    return loan_principal, annuity, number_of_months


def calculate_diff_payment(args):
    diff_payment = []
    for m in range(1, args.periods + 1):
        d = (args.principal / args.periods) + \
            (args.interest / (100 * 12)) * (args.principal -
                                            (args.principal * (m - 1) / args.periods))
        diff_payment.append(math.ceil(d))
    return tuple(diff_payment)


def calculate_overpayment(principal, repayment_sum):
    return repayment_sum - principal


def print_diff_payment(diff_payment, overpayment):
    for month, payment in enumerate(diff_payment, start=1):
        print(f"Month {month}: payment is {payment}")
    print()
    print(f"Overpayment = {overpayment}")


def get_user_input():
    parser = argparse.ArgumentParser(description="This program calculates \
    annuity or differentiated payments as well as related parameters.")

    parser.add_argument("--type",
                        choices=["annuity", "diff"],
                        help="type of payment")
    parser.add_argument("--payment",
                        type=int,
                        help="monthly payment for annuity")
    parser.add_argument("--principal",
                        type=int,
                        help="loan principal")
    parser.add_argument("--periods",
                        type=int,
                        help="number of payments")
    parser.add_argument("--interest",
                        type=float,
                        help="annual interest rate")

    # https://docs.python.org/3/library/argparse.html
    # https://www.geeksforgeeks.org/how-to-handle-invalid-arguments-with-argparse-in-python/
    # https://realpython.com/command-line-interfaces-python-argparse/
    # https://towardsdatascience.com/a-simple-guide-to-command-line-arguments-with-argparse-6824c30ab1c3

    args = parser.parse_args()

    return args


def is_input_valid(args):
    if len(vars(args)) < 4:
        return False
    if args.type is None:
        return False
    elif args.type == "diff":
        if args.payment is not None:
            return False
        if args.principal is None or args.periods is None \
                or args.interest is None:
            return False
        if args.principal < 0 or args.periods < 0 or args.interest < 0:
            return False
        return True
    elif args.type == "annuity":
        if len([x for x in [args.payment, args.principal, args.periods] if x is None]) > 1:
            return False
        if args.interest is None:
            return False
        if args.payment is None:
            if args.principal < 0 or args.periods < 0 or args.interest < 0:
                return False
        if args.principal is None:
            if args.payment < 0 or args.periods < 0 or args.interest < 0:
                return False
        if args.periods is None:
            if args.principal < 0 or args.payment < 0 or args.interest < 0:
                return False
        return True
    return False


def main():
    # python creditcalc.py --type=diff --principal=1000000 --periods=60 --interest=10
    # python creditcalc.py --type=annuity --payment=8722 --periods=120 --interest=5.6
    # python creditcalc.py --type=annuity --principal=500000 --payment=23000 --interest=5.6
    args = get_user_input()
    if is_input_valid(args):
        if args.type == "diff":
            diff_payment = calculate_diff_payment(args)
            overpayment = calculate_overpayment(args.principal, sum(diff_payment))
            print_diff_payment(diff_payment, overpayment)
        elif args.type == "annuity":
            principal, payment, periods = 0, 0, 0
            if args.payment is None:
                principal, payment, periods = calculate_payment(args)
            if args.principal is None:
                principal, payment, periods = calculate_principal(args)
            if args.periods is None:
                principal, payment, periods = calculate_periods(args)
            overpayment = calculate_overpayment(principal, payment * periods)
            print(f"Overpayment = {overpayment}")
    else:
        print("Incorrect parameters")


if __name__ == "__main__":
    main()
