from dis import Bytecode
import json
from re import X
from solcx import compile_standard, install_solc
from web3 import Web3

# Read The Sol File
with open("./code2.sol") as file:
    code2_file = file.read()

# install compiler
install_solc("0.8.7")

# compile code2_file It Returns a json object
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"code2.sol": {"content": code2_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.7",
)

# save json object in file
with open("./compiled_code2.json", "w") as file:
    if json.dump(compiled_sol, file):
        print("Json Filed Created Successfully...")

# Got ByteCode and Abi from compiled_sol
# [] Shows the structure in whixh respective values are stored
byte_code = compiled_sol["contracts"]["code2.sol"]["code2"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["code2.sol"]["code2"]["abi"]

# connecting to blockchain
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/1d84525fdebc4e768d916330cbb79e1b")
)
chainId = 4
address = "0xCC7076FAfccE2941ed6aF2089665915bb17d8b90"
private_key = "0xdb94ca50b982f927e18f45a4449a696395e97e0d880e51216a64230cedf9d606"

code2 = w3.eth.contract(abi=abi, bytecode=byte_code)

# No. Of Transaction
nonce = w3.eth.getTransactionCount(address)

# Deploying Contract
# P.S :- Always use 3<4> steps to commit a transaction
# 1> Deploy
# 2> sign
# 3> send
# 3.2> wait
transaction = code2.constructor().buildTransaction(
    {"gasPrice": w3.eth.gas_price, "chainId": chainId, "from": address, "nonce": nonce}
)

signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key
)

tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
tx_reciept = w3.eth.wait_for_transaction_receipt(tx_hash)

code_2 = w3.eth.contract(address=tx_reciept.contractAddress, abi=abi)
print("Initial Value : " + str(code_2.functions.get_n1().call()))
store_tx = code_2.functions.set_n1(45).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chainId,
        "from": address,
        "nonce": nonce + 1,
    }
)
sign_get_n1_tx = w3.eth.account.sign_transaction(store_tx, private_key=private_key)

get_n1_hash = w3.eth.send_raw_transaction(sign_get_n1_tx.rawTransaction)
tx_reciept = w3.eth.wait_for_transaction_receipt(get_n1_hash)
print("New Value : " + str(code_2.functions.get_n1().call()))
