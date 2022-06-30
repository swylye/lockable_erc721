from brownie import TestNFT, accounts, config, network, exceptions, convert
from web3 import Web3
from scripts.deploy import deploy_contract
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
import pytest
import eth_abi
import time


def test_can_mint():
    test_nft, account = deploy_contract()
    pre_mint_counter = test_nft.tokenCounter()
    tx = test_nft.mint({"from": account})
    post_mint_counter = test_nft.tokenCounter()
    assert post_mint_counter - pre_mint_counter == 1
    assert test_nft.balanceOf(account) == 1


def test_can_lock():
    test_nft, account = deploy_contract()
    account2 = get_account(name="DEV02")
    token_id = test_nft.tokenCounter()
    test_nft.mint({"from": account})
    # non token holders cannot lock
    with pytest.raises(exceptions.VirtualMachineError):
        test_nft.lockToken(token_id, account2, {"from": account2})
    # token holder can lock (if not already locked)
    test_nft.lockToken(token_id, account2, {"from": account})
    assert test_nft.tokenIdLocked(token_id) == True
    assert test_nft.tokenIdController(token_id) == account2
    # cannot lock if already locked
    with pytest.raises(exceptions.VirtualMachineError):
        test_nft.lockToken(token_id, account2, {"from": account})
    # once locked, transfer cannot be initiated from owner
    with pytest.raises(exceptions.VirtualMachineError):
        test_nft.safeTransferFrom(account, account2, token_id, {"from": account})
    # once locked approved address cannot initiate transfer as well
    test_nft.approve(account2, token_id, {"from": account})
    with pytest.raises(exceptions.VirtualMachineError):
        test_nft.safeTransferFrom(account, account2, token_id, {"from": account2})


def test_can_unlock():
    test_nft, account = deploy_contract()
    account2 = get_account(name="DEV02")
    token_id = test_nft.tokenCounter()
    test_nft.mint({"from": account})
    test_nft.lockToken(token_id, account2, {"from": account})
    # once locked non controller cannot initiate unlock
    with pytest.raises(exceptions.VirtualMachineError):
        test_nft.unlockToken(token_id, {"from": account})
    # controller can unlock token
    test_nft.unlockToken(token_id, {"from": account2})
    assert test_nft.tokenIdLocked(token_id) == False
    assert (
        test_nft.tokenIdController(token_id)
        == "0x0000000000000000000000000000000000000000"
    )
    # once unlocked, token can be transferred
    test_nft.safeTransferFrom(account, account2, token_id, {"from": account})
    assert test_nft.ownerOf(token_id) == account2
    assert test_nft.balanceOf(account) == 0
