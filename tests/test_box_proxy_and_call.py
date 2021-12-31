from brownie import network, TransparentUpgradeableProxy, ProxyAdmin, Box
from brownie.network.contract import Contract
import pytest
from scripts.helpful_scripts import get_account, upgrade, encode_function_data


def test_proxy_admin():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_intializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_intializer_function,
        {"from": account},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    assert proxy_box.retrieve() == 0
    proxy_box.store(1, {"from": account})
    assert proxy_box.retrieve() == 1

    # constructor(
    #     address _logic,
    #     address admin_,
    #     bytes memory _data
