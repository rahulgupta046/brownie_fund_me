from unittest import mock
from brownie import FundMe, MockV3Aggregator, network, config
from scripts.help_scripts import deploy_mocks, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS

def deploy_fund_me():
    account = get_account()
    #If we are not on rinkeby then deploy mocks for pricefeed address
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config['networks'][network.show_active()]['eth_usd_price_feed']
    
    else:
        deploy_mocks()
        #using the most recently deployed mock
        price_feed_address = MockV3Aggregator[-1].address
        print("Mocks deployed")

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source = config['networks'][network.show_active()].get('verify')
        )

    print(f"contract deployed to  {fund_me.address}")
    return fund_me

def main():
    deploy_fund_me()
