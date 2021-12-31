from brownie import network, TransparentUpgradeableProxy, ProxyAdmin, Box, BoxV2, exceptions
from brownie.network.contract import Contract
import pytest
from scripts.helpful_scripts import get_account, upgrade, encode_function_data


def test_proxy_admin_upgrade_boxv2():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_intitializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_intitializer_function,
        {"from": account},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    box_v2 = BoxV2.deploy({"from": account})
    upgrade_tx = upgrade(
        account, proxy, box_v2.address, proxy_admin, box_encoded_intitializer_function
    )
    upgrade_tx.wait(1)
    proxy_box_v2 = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box_v2.increment({"from": account})
    assert proxy_box_v2.retrieve() == 2
