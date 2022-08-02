from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

DECIMALS = 8  # this will be 18 for normal developemnt chiains, its 8 now because fundme had only 8 decimals
STARTING_PRICE = Web3.toWei(1762.83, 'ether')

LOCAL_BLOCKCHAIN_NETWORKS = ['development', 'ganache-local']
FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork-dev']


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_NETWORKS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])


def deploy_mocks():

    # This is done because we dont have to deploy mock every single time
    if len(MockV3Aggregator) < 1:
        print(f'The active network is {network.show_active()}')
        print('Deploying Mocks...')

        mock_aggregator = MockV3Aggregator.deploy(
            DECIMALS, STARTING_PRICE, {'from': get_account()})

        print('Deployed Mocks!')

    return MockV3Aggregator[-1].address
