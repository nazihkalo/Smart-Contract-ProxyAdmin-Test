from brownie.network import account
from scripts.helpful_scripts import encode_function_data, get_account, upgrade
from brownie import (
    network,
    Box,
    TransparentUpgradeableProxy,
    config,
    ProxyAdmin,
    Contract,
    BoxV2,
)


def deploy_proxy_and_implementation():
    account = get_account()

    # Deploy implementation contract
    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    # Deploy proxy
    proxy_admin = ProxyAdmin.deploy({"from": account})
    # Ecncode initializer function
    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    print(
        f"Proxy deployed to {proxy}, you can now updgrade the implementation contract to V2!"
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account, "gas_limit": 1000000})
    print(proxy_box.retrieve())

    box_v2 = BoxV2.deploy({"from": account})
    upgrade_tx = upgrade(
        account,
        proxy,
        box_v2.address,
        proxy_admin_contract=proxy_admin,
        initializer=None,
    )
    upgrade_tx.wait(1)
    print("Proxy has been upgraded!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    # proxy_box.store(1, {"from": account})
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve())


def main():
    deploy_proxy_and_implementation()
