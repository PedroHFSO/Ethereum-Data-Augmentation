import requests
import time
import pandas as pd
from typing import List

ETHERSCAN_API_KEY = "API_PLACEHOLDER"
BASE_URL = "https://api.etherscan.io/api"
REQUEST_DELAY = 0.25  # Etherscan limite API

def get_contract_creations(start_block: int, end_block: int) -> List[str]:
    contracts = []
    for block in range(start_block, end_block + 1):
        print(f"Lendo bloco {block}...")
        params = {
            "module": "proxy",
            "action": "eth_getBlockByNumber",
            "tag": hex(block),
            "boolean": "true",
            "apikey": ETHERSCAN_API_KEY
        }
        resp = requests.get(BASE_URL, params=params).json()
        time.sleep(REQUEST_DELAY)
        
        if "result" not in resp or resp["result"] is None:
            continue
        
        txs = resp["result"].get("transactions", [])
        for tx in txs:
            if tx["to"] is None:  # Criação de contrato inteligente                
                from_address = tx["from"]        
                contract_address = get_contract_address(tx["hash"])
                if contract_address:
                    contracts.append(contract_address)
    return contracts

def get_contract_address(tx_hash: str) -> str:
    params = {
        "module": "proxy",
        "action": "eth_getTransactionReceipt",
        "txhash": tx_hash,
        "apikey": ETHERSCAN_API_KEY
    }
    resp = requests.get(BASE_URL, params=params).json()
    time.sleep(REQUEST_DELAY)
    if resp.get("result") and resp["result"].get("contractAddress"):
        return resp["result"]["contractAddress"]
    return None

if __name__ == "__main__":
    start_block = 23410000
    end_block = 23418704
    contracts = get_contract_creations(start_block, end_block)
    df = pd.DataFrame(contracts, columns=["contractAddress"])
    df.to_csv("discovered_contracts.csv", index=False)
