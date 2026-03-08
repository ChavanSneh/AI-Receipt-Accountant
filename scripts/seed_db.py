# seed_db.py
from memory import update_system_logic

def run_seeding():
    rules = [
        "To delete an expense, navigate to the main ledger list and click the 'Delete' button next to the item.",
        "Categorize items above 100.00 as 'High Value' and flag them with a warning icon.",
        "If the AI extraction fails, the user must manually input the name and price via the 'Add Manually' form."
    ]

    print("Seeding System Vault...")
    for rule in rules:
        update_system_logic(rule)
    print("System Vault updated successfully.")

if __name__ == "__main__":
    run_seeding()