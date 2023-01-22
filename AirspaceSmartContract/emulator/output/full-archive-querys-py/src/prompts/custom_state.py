import inquirer
from .common_state import ZERO_ADDRESS
from src.utils import *
# Builds a new inquirer prompt for each required
# input for the selected smart contract method
def build_prompt(inputs, block):
    questions = []
    for inputt in inputs:
        questions.append(
            inquirer.Text(
                name=inputt["name"],
                message="Enter an {} for the {} to perform query".format(
                    inputt["type"], inputt["name"]
                ),
                default=get_default_value(inputt["type"]),
            )
        )
    questions.append(
        inquirer.Text(
            name="block",
            message="Enter the block number to perform the query",
            default=block,
        )
    )
    return questions

# Gets the user inputs required to pass as function
# parameters in the method selected for the custom contract
def get_user_input(inputs, block):
    questions = build_prompt(inputs, block)
    answers = inquirer.prompt(questions)
    block = answers["block"]
    del answers["block"]
    return list(answers.values()), block

# Returns the default value of an inquirer prompt
# based on a smart contract function input type
def get_default_value(input_type):
    if "address" in input_type:
        return ZERO_ADDRESS
    elif "uint" in input_type or "int" in input_type or "enum" in input_type:
        return "0"
    elif "bool" in input_type:
        return False
    elif "bytes" in input_type:
        return "0x0"
    elif "array" in input_type:
        return []
    elif "string" in input_type:
        return ""
    return None

# Returns the option selected to query on a custom
# smart contract. Also returns the contract methods names
# and their required inputs
def get_custom_selection():
    contract_functions = get_contract_call_methods()
    return (
        inquirer.prompt(
            [
                inquirer.List(
                    name="custom",
                    message="Choose a function from the smart contract",
                    choices=contract_functions.keys(),
                )
            ]
        )["custom"],
        contract_functions,
    )

# Performs the selection process for a method
# on the smart contract to query
def process_custom_selection(selection, contract_functions):
    latest_block = get_block_number()
    # print("Required Inputs: ", contract_functions[selection])
    inputs = contract_functions[selection]
    user_inputs, block = get_user_input(inputs, latest_block)
    # print("inputs: ", user_inputs)
    if len(inputs) < 1:
        call_contract_function_without_params(selection, block)
    else:
        call_contract_function_with_params(selection, user_inputs, block)
