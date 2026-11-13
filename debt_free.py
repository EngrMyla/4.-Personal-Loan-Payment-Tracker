#Debt Free Program#
import os
import subprocess
from pathlib import Path

from svg_generator import generate_svg_summary, MIN_VISIBLE_ROWS, MAX_VISIBLE_ROWS


debt_free = {}


## Helper Functions
def check_positive_float(value):
    try:
        num_value = float(value)
        if num_value <= 0:
            raise ValueError("Value must be greater than zero.")
        return num_value
    except (TypeError, ValueError):
        print("Invalid input: Please enter a valid number greater than zero.")
        return None

def show_svg_location(svg_path):
    svg_path = Path(svg_path)
    print("\nSVG report generated successfully.")
    print(f"Open this file: {svg_path}")

    vsc_path = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Programs",
        "Microsoft VS Code",
        "bin",
        "code.cmd"
    )

    attempts = [
        ["code", "--reuse-window", str(svg_path)],
        ["code.cmd", "--reuse-window", str(svg_path)],
    ]

    if os.path.exists(vsc_path):
        attempts.insert(0, [vsc_path, "--reuse-window", str(svg_path)])

    for cmd in attempts:
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Opened in VS Code.")
            return
        except Exception:
            pass

    try:
        os.startfile(str(svg_path))
        print("Opened with default app.")
        return
    except Exception:
        pass

    try:
        import webbrowser
        webbrowser.open(svg_path.resolve().as_uri())
        print("Opened in browser.")
    except Exception:
        print(f"Open in browser: {svg_path.resolve().as_uri()}")

## Core Functions
# 1. Track your debt
def track_debt():
    print("\n***Track your Debt***")

    while True:
        bank_name = input("\nEnter the bank name: ").strip().upper()
        if not bank_name:
            print("Bank name cannot be empty.")
            continue

        if bank_name in debt_free:
            current_original_debt = debt_free[bank_name]["original_debt"]

            print(f"Existing record found: {bank_name} - Debt: P{current_original_debt:.2f}")

            modify_record = input("Do you want to modify this debt record? (y/n): ").strip().lower()
            if modify_record != 'y':
                print(f"No changes made to {bank_name}.")
            else:
                update_debt_amount = input("Do you want to update the debt amount? (y/n): ").strip().lower()
                if update_debt_amount == 'y':
                    new_original_debt = check_positive_float(input("Enter the new debt amount: "))
                    if new_original_debt is None:
                        continue
                    debt_free[bank_name]["original_debt"] = new_original_debt

                updated_original_debt = debt_free[bank_name]["original_debt"]
                print(f"Updated record: {bank_name} - Debt: P{updated_original_debt:.2f}")

            more_debts = input("\nDo you want to add more debts? (y/n): ")
            if more_debts.lower() != 'y':
                break
            continue

        original_debt_amount = check_positive_float(input("Enter the amount owed: "))
        if original_debt_amount is None:
            continue

        debt_free[bank_name] = {
            "original_debt": original_debt_amount,
            "amount_paid": 0.0,
        }

        print(f"Debt recorded: {bank_name} - Debt: P{original_debt_amount:.2f}")

        more_debts = input("\nDo you want to add more debts? (y/n): ")
        if more_debts.lower() != 'y':
            break

# 2. View your debt summary
def view_summary():
    print("\n***Debt Summary***")
    if not debt_free:
        print("No debts recorded.")
        return

    ranked_debts = sorted(
        debt_free.items(),
        key=lambda item: item[1]["original_debt"],
        reverse=True
    )

    for index, (bank_name, debt_record) in enumerate(ranked_debts, start=1):
        original_debt_amount = debt_record["original_debt"]
        amount_paid = debt_record["amount_paid"]
        current_balance = original_debt_amount - amount_paid
        print(
            f"{index}. {bank_name} - Debt: P{original_debt_amount:.2f} - "
            f"Balance: P{current_balance:.2f}"
        )

# 3. Record your payment history
def record_payment():
    print("\n***Record Payment***")

    while True:
        if not debt_free:
            print("No debts recorded.")
            return

        print("\nCurrent debt records:")
        ranked_debts = sorted(
            debt_free.items(),
            key=lambda item: item[1]["original_debt"],
            reverse=True
        )

        for index, (bank_name, debt_record) in enumerate(ranked_debts, start=1):
            current_balance = debt_record["original_debt"] - debt_record["amount_paid"]
            print(
                f"{index}. {bank_name} - Balance: P{current_balance:.2f} "
                f"(Debt: P{debt_record['original_debt']:.2f})"
            )

        bank_names = [bank_name for bank_name, _ in ranked_debts]
        print("\nSelect a bank to pay:")
        for index, bank_name in enumerate(bank_names, start=1):
            print(f"{index}. {bank_name}")

        while True:
            selection = input("\nEnter the number of the bank you want to pay: ").strip()
            try:
                bank_index = int(selection)
            except ValueError:
                print("Invalid input. Please enter a number from the list.")
                continue

            if 1 <= bank_index <= len(bank_names):
                bank_name = bank_names[bank_index - 1]
                break

            print(f"Please enter a number between 1 and {len(bank_names)}.")

        current_balance = debt_free[bank_name]["original_debt"] - debt_free[bank_name]["amount_paid"]
        if current_balance <= 0:
            print(f"{bank_name} already has no outstanding balance.")
            another_payment = input("Do you want to record another payment? (y/n): ").strip().lower()
            if another_payment != 'y':
                return
            continue

        print(f"\nSelected bank: {bank_name}")
        print(f"Outstanding balance: P{current_balance:.2f}")

        payment_amount = check_positive_float(input("Enter the payment amount: "))
        if payment_amount is None:
            continue

        if payment_amount > current_balance:
            print(f"Payment amount exceeds the outstanding debt. Maximum payment: P{current_balance:.2f}")
            continue

        debt_free[bank_name]["amount_paid"] += payment_amount
        remaining_balance = debt_free[bank_name]["original_debt"] - debt_free[bank_name]["amount_paid"]
        print(
            f"Payment recorded: {bank_name} - "
            f"Amount paid: P{payment_amount:.2f} - Remaining balance: P{remaining_balance:.2f}"
        )

        another_payment = input("\nDo you want to record another payment? (y/n): ").strip().lower()
        if another_payment != 'y':
            return

# 4. Publish your debt-free journey for the month
def publish_journey():
    print("\n***Publish Debt-Free Journey***")
    if not debt_free:
        print("No debts recorded.")
        return

    print(f"Note: SVG summary shows a minimum of {MIN_VISIBLE_ROWS} and a maximum of {MAX_VISIBLE_ROWS} entries.")
    print("Your debt-free journey for the month:")
    for bank_name, debt_record in debt_free.items():
        original_debt_amount = debt_record["original_debt"]
        amount_paid = debt_record["amount_paid"]
        current_balance = original_debt_amount - amount_paid
        print(f"{bank_name}: P{current_balance:.2f}")

    svg_path = generate_svg_summary(debt_free)
    show_svg_location(svg_path)

# Main Menu Functions

def menu():
    while True:
        print("\nWelcome to the Debt Free Program!")
        print("1. Track your debt")
        print("2. View your debt summary")
        print("3. Record your payment history")
        print("4. Publish your debt-free journey for the month")
        print("5. Exit")

        choice = input("\nPlease select an option (1-5): ")
        if choice == '1':
            track_debt()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            record_payment()
        elif choice == '4':
            publish_journey()
        elif choice == '5':
            print("\nThank you for using the Debt-Free App. You can do it!\n")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    menu()