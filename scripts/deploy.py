from brownie import TestNFT, config, network
from scripts.helpful_scripts import get_account
import time


def main():
    test_nft, account = deploy_contract()


def deploy_contract():
    account = get_account()
    # if len(TestNFT) > 0:
    #     test_nft = TestNFT[-1]
    # else:
    #     test_nft = TestNFT.deploy(
    #         {"from": account},
    #         publish_source=config["networks"][network.show_active()].get(
    #             "verify", False
    #         ),
    #     )
    test_nft = TestNFT.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    return test_nft, account
