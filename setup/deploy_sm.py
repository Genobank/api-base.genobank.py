#!/usr/bin/env python3
import json
import os
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware
from settings import settings

def load_contract_interface(path):
    with open(path, 'r') as f:
        data = json.load(f)
    abi = data.get('abi')
    bytecode = data.get('bin')
    if not abi or not bytecode:
        raise RuntimeError(f"Could not extract abi/bytecode from {path}")   
    return abi, bytecode

def deploy_contract(w3, json_path, constructor_args):
    abi, bytecode = load_contract_interface(json_path)
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    tx = contract.constructor(*constructor_args).buildTransaction({
        'from': w3.eth.default_account,
        'nonce': w3.eth.getTransactionCount(w3.eth.default_account),
        'gas': 5_000_000,
        'gasPrice': w3.toWei('20', 'gwei'),
    })
    signed = w3.eth.account.sign_transaction(tx, settings.EXECUTOR_PRIVATE_KEY)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
    print(f"→ Deploying {os.path.basename(json_path)}  tx: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    addr = receipt.contractAddress
    print(f"✓ Deployed at {addr}\n") 
    return addr


def update_env_file(addresses):
    env_path = settings.OUTPUT_ENV_FILE_NAME
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"Env file not found: {env_path}")
    with open(env_path, 'r') as f:
        lines = f.readlines()
    keys = addresses.keys()
    seen = {k: False for k in keys}
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if '=' in stripped:
            key = stripped.split('=')[0].strip()
            if key in addresses:
                new_lines.append(f'{key} = "{addresses[key]}"\n')
                seen[key] = True
                continue
        new_lines.append(line)
    for key, addr in addresses.items():
        if not seen[key]:
            new_lines.append(f"{key} = {addr}\n")
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
    print(f"✔ {env_path} updated with contract addresses.")


def main():
    w3 = Web3(HTTPProvider(settings.PROVIDER))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    acct = w3.eth.account.from_key(settings.EXECUTOR_PRIVATE_KEY)
    w3.eth.default_account = acct.address
    print(f"Deploying account: {acct.address}\n")
    addresses = {}
    addresses['BPT_CONTRACT'] = deploy_contract(
        w3, settings.ABI_BPT_PATH,
        [settings.BPT_NAME, settings.BPT_SYMBOL, settings.BPT_NAMESPACE]
    )
    addresses['xBPT_CONTRACT'] = deploy_contract(
        w3, settings.ABI_XBPT_PATH,
        [settings.XBPT_NAME, settings.XBPT_SYMBOL]
    )
    addresses['BIOSAMPLE_CONTRACT'] = deploy_contract(
        w3, settings.ABI_BIOSAMPLE_PATH,
        [settings.BIOSAMPLE_URI]
    )
    addresses['POSP_FACTORY_CONTRACT'] = deploy_contract(
        w3, settings.ABI_POSP_FACTORY_PATH, []
    )
    addresses['DELIVER_MANAGER_CONTRACT'] = deploy_contract(
        w3, settings.ABI_DELIVER_MANAGER_PATH,
        [settings.USDNA_CONTRACT]
    )
    update_env_file(addresses)

if __name__ == "__main__":
    main()