import inquirer
from src.utils import *
from operator import itemgetter
LATEST_BLOCK = ""
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
# Builds a prompt for block input
def block_prompt():
    LATEST_BLOCK = get_block_number()
    return inquirer.Text(
        "block",
        message="Enter the block number to perform the query (blank to use latest block)",
        default=LATEST_BLOCK,
    )

# Builds a prompt for address input
def address_prompt():
    return inquirer.Text(
        "address",
        message="Enter an address to perfom the query (blank to use zero address)",
        default=ZERO_ADDRESS,
    )

#  Prompts the inputs for the block to query transactions
#  and select if go full details or just the hashes
def get_block_full():
    questions = [
        block_prompt(),
        inquirer.Confirm(
            "full",
            message="Do you wish to get the full transactions output",
            default=False,
        ),
    ]
    return inquirer.prompt(questions)

# Prompts the inputs for the block
# and the address to perform a query
def get_address_block():
    questions = [address_prompt(), block_prompt()]
    return inquirer.prompt(questions)

# Prompts the inputs for the block, address
# and the position to perform a query
def get_address_block_position():
    questions = [
        address_prompt(),
        block_prompt(),
        inquirer.Text(
            "position",
            message="Enter the position of the storage to perform the query (default 0)",
            default="0",
        ),
    ]
    return inquirer.prompt(questions)

# Performs query for getting ETH balance
def process_eth_balance():
    address, block = itemgetter("address", "block")(get_address_block())
    address = to_checksum_address(address)
    print_eth_balance_of(address, int(block))
    return

# Performs query for getting code at given address
def process_storage_at():
    address, block, position = itemgetter("address", "block", "position")(
        get_address_block_position()
    )
    address = to_checksum_address(address)
    print_storage_at(address, int(position), int(block))

# Performs query for getting storage at an address
# at a given position
def process_code_at():
    address, block = itemgetter("address", "block")(get_address_block())
    address = to_checksum_address(address)
    print_code_at(address, int(block))

# Performs query for getting a block transactions
def process_transactions():
    block, full = itemgetter("block", "full")(get_block_full())
    print_block_transactions(int(block), full)

# Prompts the option to select the common state
# query function to call
def get_commons_selection():
    return inquirer.prompt(
        [
            inquirer.List(
                "commons",
                message="Select a common query to perform",
                choices=[
                    "Get ETH balance of an address at a given block",
                    "Get storage at an address at a given position and block",
                    "Get code of an address at a given block",
                    "Get block transactions from a given block",
                ],
            )
        ]
    )["commons"]

# Executes the method select on CLI
def process_commons_selection(selection):
    if "balance" in selection:
        process_eth_balance()
    elif "code" in selection:
        process_code_at()
    elif "storage" in selection:
        process_storage_at()
    elif "transactions" in selection:
        process_transactions()
