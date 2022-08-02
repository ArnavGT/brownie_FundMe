from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_NETWORKS, deploy_mocks, FORKED_LOCAL_ENVIRONMENTS
from brownie import network, accounts, exceptions
from scripts.deploy import deploy_fundme
import pytest


def test_can_fund_withdraw():
    account = get_account()
    fund_me = deploy_fundme()
    entrance_Fee = fund_me.getEntranceFee()

    tx = fund_me.fund({'from': account, 'value': entrance_Fee * 10**10})
    tx.wait(1)

    assert fund_me.AddressToFunds(account.address) == entrance_Fee * 10**10

    tx2 = fund_me.withdraw({'from': account})
    tx2.wait(1)

    assert fund_me.AddressToFunds(account.address) == 0


def test_only_owner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pytest.skip("Only for Local testing")
    fund_me = deploy_fundme()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({'from': bad_actor})
