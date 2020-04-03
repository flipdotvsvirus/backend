"""Takes a string copied from excel online and calculates how much everyone must pay"""
import numpy as np


def main():
    credits = input('Paste your current values from excel: ').replace('€', '').split('\t')
    credits = [x.strip().split(',') for x in credits]
    credits = [int(x[0]) * 100 + int(x[1]) if len(x[1]) == 2 else None for x in credits]
    if not all([x is not None for x in credits]):
        print(credits)
        raise ValueError('Some values are wrong. Make sure your format is "xxx,yy €", separated by tab')
    amount_ok = False
    while not amount_ok:
        withdraw_amount = input('How much money should be withdrawn? (format: xxx,yy) ').split(',')
        amount_ok = len(withdraw_amount) == 2 and len(withdraw_amount[1]) == 2
    withdraw_amount = int(withdraw_amount[0]) * 100 + int(withdraw_amount[1])
    new_credits = withdraw(withdraw_amount, np.array(credits))
    print('New Credits:')
    euros, cents = new_credits // 100, new_credits % 100
    print('\t'.join([f'{e},{c:02} €' for e, c in zip(euros, cents)]))


def withdraw(amount: int, credits: np.array):
    if amount > sum(credits):
        raise ValueError("Sorry, we don't have enough money to pay that :(")
    new_credits = credits.copy()
    number_of_positive_accounts = len(credits[credits > 0])

    if amount < number_of_positive_accounts:
        return withdraw_rest_from_random_credits(amount, new_credits)

    amount_per_participant = amount // number_of_positive_accounts
    # The amount may not be equally distributable between the participants.
    # In this case the missing amount must be distributed between fewer participants
    amount_rest = amount % number_of_positive_accounts

    new_credits[credits > 0] -= amount_per_participant
    negative_amounts = new_credits[new_credits < 0]
    remaining_amount = -sum(negative_amounts) + amount_rest
    new_credits[new_credits < 0] = 0
    # remaining_credits = new_credits[new_credits >= 0]
    if remaining_amount:
        new_credits = withdraw(remaining_amount, new_credits)
    return new_credits


def withdraw_rest_from_random_credits(amount: int, credits: np.array):
    extra_payment = np.zeros(credits.shape, dtype=int)
    extra_payment[np.random.choice(np.where(credits > 0)[0], amount, replace=False)] = 1
    return credits - extra_payment


if __name__ == '__main__':
    main()
