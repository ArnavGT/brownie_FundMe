from brownie import FundMe, network
from scripts.deploy import deploy_fundme
from scripts.helpful_scripts import get_account


def fund():
    fund_me = deploy_fundme()
    account = get_account()

    entranceFee = fund_me.getEntranceFee()
    print(f"This is the entrance Fee: {entranceFee * 10**10}")
    print('Funding')

    # Any low level function parameters that we have to send such as paying a payable function or anything else
    # We send it via the dictionary.
    fund_me.fund({'from': account, 'value': entranceFee * 10 ** 10})

    print('Funded! Thank you.')


def withdraw():
    print('Withdrawing...')

    account = get_account()
    fund_me = FundMe[-1]
    fund_me.withdraw({'from': account})

    print('Withdrawn! Thank you.')


def main():
    fund()
    withdraw()
