import requests
import time
import pandas as pd

ETHERSCAN_API_KEY = "API_PLACEHOLDER"
BASE_URL = "https://api.etherscan.io/api"
REQUEST_DELAY = 0.25  # Etherscan limite API


def get_contract_bytecode(address: str) -> str:    
    params = {
        "module": "proxy",
        "action": "eth_getCode",
        "address": address,
        "tag": "latest",
        "apikey": ETHERSCAN_API_KEY
    }
    resp = requests.get(BASE_URL, params=params)
    data = resp.json()
    time.sleep(REQUEST_DELAY)
    return data.get("result", "")


def enrich_with_bytecode(input_csv: str, output_csv: str):    
    df = pd.read_csv(input_csv)
    bytecodes = []
    for addr in df["contractAddress"]:
        print(f"Buscando bytecode de {addr}...")
        bytecode = get_contract_bytecode(addr)
        bytecodes.append(bytecode)

    df["bytecode"] = bytecodes
    df.to_csv(output_csv, index=False)


if __name__ == "__main__":
    enrich_with_bytecode("discovered_contracts.csv", "contracts_with_bytecode.csv")
