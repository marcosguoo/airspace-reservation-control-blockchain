import inquirer
from src.prompts.custom_state import *
from src.prompts.common_state import *
# Prompts the main selection panel
def get_selection():
    questions = [
        inquirer.List(
            "main query",
            message="Select the type of functions to query",
            choices=[
                "Common state functions (get_balance, get_block,...)",
                "Custom contract state functions",
            ],
        )
    ]
    answers = inquirer.prompt(questions)
    if "Common" in answers["main query"]:
        selection = get_commons_selection()
        process_commons_selection(selection)
    else:
        selection, contract_functions = get_custom_selection()
        process_custom_selection(selection, contract_functions)
