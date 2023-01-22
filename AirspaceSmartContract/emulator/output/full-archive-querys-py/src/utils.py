# Imports
import json
from web3 import Web3
from pprint import pprint
# Init full and archive provider
full_node_provider = Web3(
    Web3.HTTPProvider(
        "http://localhost:8545"
    )
)
archive_node_provider = Web3(
    Web3.HTTPProvider(
        "http://localhost:8545"
    )
)

def to_checksum_address(address):
    return full_node_provider.toChecksumAddress(address)

def to_hex(string):
    return full_node_provider.toHex(string)

# Returns the current block number of a network
def get_block_number():
    return full_node_provider.eth.block_number

# Returns the ETH balance of a given address at a given block
def get_eth_balance(address, block):
    print(
        "[QUERYING] Fetching ETH balance from address {} at block {}".format(
            address, block
        )
    )
    try:
        print("[QUERYING] Attempting with full Node")
        return full_node_provider.eth.get_balance(address, block)
    except Exception as e:
        if "missing trie node" in str(e):
            print("[OLD-BLOCK-QUERY] Switching to archive query")
            return archive_node_provider.eth.get_balance(address, block)
        else:
            print("exception: ", e)
            return None

# Returns the storage of an address at a given position and block
def get_storage_at(address, position, block):
    try:
        print(
            "[QUERYING] Fetching storage at address {} at position {} at block {}".format(
                address, position, block
            )
        )
        return full_node_provider.eth.get_storage_at(address, position, block)
    except Exception as e:
        if "missing trie node" in str(e):
            print("[OLD-BLOCK-QUERY] Switching to archive query")
            return archive_node_provider.eth.get_storage_at(address, position, block)
        else:
            return None

# Returns the code at a given address and block
def get_code(address, block):
    try:
        print(
            "[QUERYING] Fetching code at address {} at block {}".format(address, block)
        )
        return full_node_provider.eth.get_code(address, block)
    except Exception as e:
        if "missing trie node" in str(e):
            print("[OLD-BLOCK-QUERY] Switching to archive query")
            return archive_node_provider.eth.get_code(address, block)
        else:
            return None

# Returns the mined transactions in a given block
def get_block_transactions(block, full_transactions=False):
    try:
        print("[QUERYING] Fetching transactions from block {}".format(block))
        return full_node_provider.eth.get_block(block, full_transactions)
    except Exception as e:
        if "missing trie node" in str(e):
            print("[OLD-BLOCK-QUERY] Switching to archive query")
            return archive_node_provider.eth.get_block(block, full_transactions)
        else:
            return None

def print_eth_balance_of(address, block):
    eth_balance = get_eth_balance(address, block)
    print(
        "[BALANCE-RESULTS] Eth balance of address {} at block {}: {} $ETH".format(
            address, block, eth_balance
        )
    ) if eth_balance is not None else print("Invalid Query")

def print_storage_at(address, position, block):
    storage_at = full_node_provider.toHex(get_storage_at(address, position, block))
    print(
        "[STORAGE-AT-RESULTS] Storage at {} at position {} at block {}: {}".format(
            address, position, block, storage_at
        )
    ) if storage_at is not None else print("Invalid query")

def print_code_at(address, block):
    code_at = full_node_provider.toHex(get_code(address, block))
    print(
        "[CODE-AT-RESULTS] Code at address {} at block {}: {}".format(
            address, block, code_at
        )
    ) if code_at is not None else print("Invalid query")

def print_block_transactions(block, full):
    block_transactions = get_block_transactions(block, full)
    print(
        "[TRANSACTIONS] Transactions at block {}: {}".format(block, block_transactions)
    ) if block_transactions is not None else print("Invalid Query")

########## SMART CONTRACT INTERACTIONS ##############
CONTRACT_ADDRESS = "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE"
with open("src/abi.json") as f:
    abi = json.load(f)
full_node_contract = full_node_provider.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
archive_node_contract = archive_node_provider.eth.contract(
    address=CONTRACT_ADDRESS, abi=abi
)

def get_contract_call_methods():
    pprint(full_node_contract.functions._functions)
    print(type(full_node_contract.functions._functions))
    view_functions = {}
    for function in full_node_contract.functions._functions:
        # print(function)
        if function["stateMutability"] == "view":
            view_functions[function["name"]] = function["inputs"]
    return view_functions
