import calendar
import datetime
from expense import Expense
import sys

print("--------------------------------------")
print("Expense tracking program is running")
print("--------------------------------------")


def main():
    while True: 
        expense_file = "expense.csv"

        expense = expense_input()
        print("--------------------------------------")
        print(f"Expense is {expense}")
        print("--------------------------------------\n")

        saving_data_to_file(expense, expense_file)
        print("--------------------------------------\n")

        expense_summary(expense_file)

        choices(expense_file)

        break

def get_budget():
    try: 
        budget = float(input("\nEnter your budget for the month: $"))
        return budget
    except ValueError:
        print("Invalid input. Please enter numeric value.")
        return get_budget()

def get_data_from_file(expense_file):
    expenses : list[Expense] = []
    with open(expense_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            if not line.strip():
                continue
            expense_name, expense_amount, expense_category, expense_date = line.strip().split(",")
            line_expense =Expense(name=expense_name, amount=float(expense_amount), category=expense_category, date=expense_date)
            expenses.append(line_expense)
    return expenses

def input_date():
    date_input = (input("Enter the date(YYYY-MM-DD) or press 'Enter' for today:"))
    date_spent_on = ""
    if date_input.strip():
        try: 
            date_spent_on = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
            print(f"Date entered: {date_spent_on}")
        except ValueError:
            print("Invalid date format. Please try again.")
            return date_input

    else :
        date_spent_on = datetime.date.today()
        print(f"Today's date: {date_spent_on}")
    
    return date_spent_on

def expense_input():
    try: 
        expense_name = (input("Enter expense name (what you spent on):"))   
        amount_spent = float(input("Enter the amount you spent: $"))

        date_spent_on = input_date()
        
        print(f"You have entered {expense_name}, ${amount_spent}, {date_spent_on}")
        # static categories to reduce complication
        expense_category_list = [
            "Home",
            "Food", 
            "Health",
            "Fashion",
            "Transportation", 
            "Subscription", 
            "Fun",
        ]

        while True:
            print("Select a category:")
            for i, category_name in enumerate(expense_category_list):
                print(f" {i+1}. {category_name}")

            value_range = f"[1 - {len(expense_category_list)}]"
            selected_index = int(input(f"Enter a category number {value_range}:")) -1 
            if selected_index in range(len(expense_category_list)):
                selected_category = expense_category_list[selected_index]
                new_expense = Expense(name=expense_name, category=selected_category,amount=amount_spent, date=date_spent_on)
                return new_expense
            else: 
                print("Invalid category. Please try again.")
                
    except ValueError:
        print("Invalid input. Please try again.")
        return expense_input()

def saving_data_to_file(expense: Expense, expense_file):
    print(f"Saving {expense} to {expense_file}")
    with open(expense_file, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category},{expense.date} \n")


def expense_summary(expense_file):
    expenses = get_data_from_file(expense_file)

    # create a dictionary for category to see which is the most spent
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
    print("Expenses by category:\n")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    total = sum([x.amount for x in expenses])
    print(f"\nTotal spent: ${total:.2f}")

    budget = get_budget()
    remaining_budget = budget - total
    print(f"\n Remaining budget: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(f"\n To last throughout the month, the daily budget recommendation would be: ${daily_budget:.2f}")

def editing_expense(expense_file):
    try: 
        print("\n".join(map(str, load_expense(expense_file))))
        expenses = get_data_from_file(expense_file) #print old expense
        expense_to_edit = input("Enter expense name you want to edit: ").strip().lower()
        for expense in expenses:
            if expense_to_edit in expense.name.lower():
                expense.name = input(f"Enter new name for [{expense.name}]: ").strip() or expense.name
                expense.amount = float(input(f"Enter new price [{expense.amount}]: ") or expense.amount)
                expense.category = input(f"Enter new category [{expense.category}]: ").strip() or expense.category
                new_date = input_date()
                expense.date = new_date
                break
        else:
            print("Expense not found.")
        print("is expense correct", expenses)
        save_after_edit(expense_file, expenses)
    except Exception:
        print("Invalid input. Try again.")
        return editing_expense()
    
def load_expense(expense_file):
    try:
        expenses = get_data_from_file(expense_file)
        return expenses
    except FileNotFoundError:
        print("No expense file found. Starting fresh.")
        return []

def save_after_edit(expense_file, expenses):
    with open(expense_file, "w") as f:
        for exp in expenses:
            print(exp)
            f.write(f"{exp.name},{exp.amount},{exp.category},{exp.date}\n")

def choices(expense_file):
    try: 
        while True: 
            action = input("\n Do you want to: \n 1. Edit expense \n 2. Continue Program \n 3. Exit program ? Enter your choices (1, 2 or 3):")
            if action == "1":
                editing_expense(expense_file)
                print("Expense saved to csv file.")
                expense_summary(expense_file)
            elif action == "2":
                print("--------------------------------------\n")
                main() 
            elif action == "3":
                return exit()
            else: 
                print("Invalid choice. Try again. ")
    except Exception:
        print("Invalid numberic input. Please try again.")
        return choices(expense_file)

def exit():
    print("Exiting program.")
    sys.exit(0)

if __name__ == "__main__":
    main()