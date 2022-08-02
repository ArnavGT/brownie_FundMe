from brownie import config, FundMe, MockV3Aggregator, network
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_NETWORKS


def get_pf_address(account):
    # If we are not in development, use the address for the required network
    if network.show_active() not in LOCAL_BLOCKCHAIN_NETWORKS:
        pf_address = config['networks'][network.show_active()
                                        ]['eth_usd_price_feed']
        return pf_address

    else:  # If we are in develpoment, deploy mocks.
        return deploy_mocks()


def deploy_fundme():
    account = get_account()

    fundme = FundMe.deploy(get_pf_address(account),
                           {'from': account},
                           publish_source=config['networks'][network.show_active()].get('verify'))
    # If we have to pass a variable onto our constructor, we can pass it through contract deployment.
    # This will not only deploy the contract, but also verify and publish the contract in etherscan website so that we can interact with it.

    print(f'Contract deployed to {fundme.address}!')
    print(f'Balance is {account.balance()}')
    return fundme


def main():
    deploy_fundme()
