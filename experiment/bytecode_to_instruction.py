import pandas as pd
import pyevmasm

def bytecode_to_instructions(bytecode: str) -> str:
    try:
        # Forçar início com 0x+
        if not bytecode.startswith("0x"):
            bytecode = "0x" + bytecode

        code_bytes = bytes.fromhex(bytecode[2:])
        instructions = [ins.mnemonic for ins in pyevmasm.disassemble_all(code_bytes)]
        return " ".join(instructions)
    except Exception as e:
        print(f"Erro convertendo bytecode: {e}")
        return ""

def enrich_with_instructions(input_csv: str, output_csv: str):
    df = pd.read_csv(input_csv)
    df["instructions"] = df["bytecode"].apply(bytecode_to_instructions)
    df.to_csv(output_csv, index=False)


# ------------------- USAGE -------------------
if __name__ == "__main__":
    enrich_with_instructions("contracts_with_bytecode.csv", "contracts_with_instructions.csv")
