from typing import List, Optional
import csv

CSV_FILENAME = 'wydatki.csv'

class Transaction:
    next_id = 1

    def __init__(self, description: str, value: float):
        self.id = Transaction.next_id  
        Transaction.next_id += 1  
        self.description = description
        self.value = value
        self.type_ = self.__class__.__name__


    def __str__(self):
        return f"{self.id:<2}. {self.value:>10.2f} | {self.description}  " 
    

    def __repr__(self):
        return f"{self.__class__.__name__}id={self.id!r}, description={self.description!r}, value={self.value!r})"
    

    def __eq__(self, other: "Transaction") -> bool:
        return self.value == other.value

    def __gt__(self, other: "Transaction") -> bool:
        return self.value > other.value

    def __lt__(self, other: "Transaction") -> bool:
        return self.value < other.value

    @staticmethod
    def validate_description(description: str) -> str:
        """Checks that the description is not empty"""
        description = description.strip()
        if not description:
            raise ValueError("Błąd! Opis nie może być pusty.")
        return description
    

    @staticmethod
    def validate_value(value: str) -> float:
        try:
            value = float(value.strip())
            if value <= 0:
                raise ValueError("Błąd! Wartość musi być większa od 0.")
            return value
        except ValueError:
            raise ValueError("Błąd! Wartość musi być liczbą większa od 0.")
        
    @staticmethod
    def total_value(transactions: List["Transaction"]) -> float:
        """Zwraca sumę wartości dla listy transakcji."""
        return sum(transaction.value for transaction in transactions)
    

    @staticmethod
    def compare_expenses_vs_income(transactions: List["Transaction"]) -> str:
        """Porównuje sumę wydatków i przychodów."""
        sum_income = Transaction.total_value([t for t in transactions if isinstance(t, Income)])
        sum_expense = Transaction.total_value([t for t in transactions if isinstance(t, Expense)])

        if sum_income > sum_expense:
            return f"\nPrzychody ({sum_income:.2f} PLN) są większe od wydatków ({sum_expense:.2f} PLN)."
        elif sum_income < sum_expense:
            return f"\nWydatki ({sum_expense:.2f} PLN) są większe od przychodów ({sum_income:.2f} PLN)."
        else:
            return f"\nPrzychody i wydatki są równe ({sum_income:.2f} PLN)."

        

    @classmethod
    def from_user_input(cls) -> "Transaction":
        """Creates a new transaction based on the data entered by the user."""
        while True:
            try:
                description = cls.validate_description(input("Podaj opis: "))
                value = cls.validate_value(input("Podaj wartość: "))
                indicator = input("Określ czy to jest przychód czy wydatek? [p/w]").lower().strip()

                if indicator == 'p':
                    return Income(description, value)
                elif indicator == 'w':
                    return Expense(description, value)
                else:
                    return "Błąd! Wybierz 'p' dla przychodu lub 'w' dla wydatku."
                
            except ValueError as e:
                print(e)

    def finding_transaction(transactions: List["Transaction"], user_id_choice: int) -> Optional["Transaction"]:
        for transaction in transactions:
            if transaction.id == user_id_choice:
                return transaction
        return None
    

    def deleting_from_list(self, transactions: List["Transaction"]) -> str:
        user_approval = input(f"Czy potwierdzasz usunięcie {self} z bazy? [t/n]").lower()
        if user_approval == 't':
            transactions.remove(self)
            return f"Usunięto transakcję: {self}"
        return "Anulowano wybór"
    


class Expense(Transaction):
    def indication(self):
        print('Wydatek')


class Income(Transaction):
    def indication(self):
        print('Przychód')    



def menu_printing() -> None:
    print("\nWybierz co chcesz zrobić")
    print("1. Dodaj nową transakcję")
    print("2. Usuń wybraną transakcję")
    print("3. Wyświetl wszystkie transakcje")
    print("4. Zmodyfikuj wybraną transakcję")
    print("5. Zaimportuj transakcje z bazy")
    print("6. Zapisz zmiany w bazie danych")
    print("7. Zakończ program\n")


def display_transactions(transactions: List[Transaction]) -> None:
    if not transactions:
        print("\nBrak zapisanych transakcji do wyświetlenia.")
        return
    
    incomes = [t for t in transactions if isinstance(t, Income)]
    expenses = [t for t in transactions if isinstance(t, Expense)]

    print("\n PRZYCHODY:")
    print("-" * 40)
    for income in incomes:
        print(f"{income.id:<5} {income.value:>10.2f} PLN | {income.description}")

    print("\n WYDATKI:")
    print("-" * 40)
    for expense in expenses:
        print(f"{expense.id:<5} {expense.value:>10.2f} PLN | {expense.description}")

    print("-" * 40)

    sum_income = Transaction.total_value([t for t in transactions if isinstance(t, Income)])
    sum_expense = Transaction.total_value([t for t in transactions if isinstance(t, Expense)])
    print(f"\nSuma przychodów: {sum_income:.2f} PLN")
    print(f"Suma wydatków: {sum_expense:.2f} PLN")
    print()
    print(Transaction.compare_expenses_vs_income(transactions))

                   
def select_transaction(transactions: List[Transaction], action: str) -> Optional[Transaction]:
    if not transactions:
        print(f"\nBrak transakcji do {action}.")
        return None

    print(f"\nDostępne ID transakcji do {action}:")
    for transaction in transactions:
        print(f"{transaction.id:<3}: {transaction.value:>10.2f} | {transaction.description}")

    try:
        id_choice = int(input(f"Wybierz nr ID transakcji, którą chcesz {action}: "))
        transaction = Transaction.finding_transaction(transactions, id_choice)
        if transaction:
            return transaction
        else:
            print("Błąd! Nie znaleziono transakcji o podanym ID.")
            return None
    except ValueError:
        print("Błąd! Wpisz poprawny numer ID.")
        return None


def deleting_transaction(transactions: List[Transaction]) -> None:
    transaction_to_remove = select_transaction(transactions, "usunąć")
    if transaction_to_remove:
        print(transaction_to_remove.deleting_from_list(transactions))
    
    

def modifying_transaction(transactions: List[Transaction]) -> None:
    transaction_to_modify = select_transaction(transactions, "zmodyfikować")
    
    if transaction_to_modify:
        print(f"\nObecna transakcja: {transaction_to_modify}")
        
        print("\nCo chcesz zmodyfikować?")
        print("1: Opis\n2: Wartość\n3: Anuluj")
        choice = input("Wybierz opcję: ").strip()
        
        if choice == "1":
            new_description = input("Podaj nowy opis: ").strip()
            transaction_to_modify.description = new_description
        elif choice == "2":
            try:
                new_value = float(input("Podaj nową wartość: ").strip())
                if new_value <= 0:
                    print("Błąd! Wartość musi być większa od 0.")
                else:
                    transaction_to_modify.value = new_value
            except ValueError:
                print("Błąd! Wpisz poprawną liczbę.")
        elif choice == "3":
            print("Anulowano modyfikację.")
        else:
            print("Błąd! Wybierz poprawną opcję.")

        print(f"\nZmodyfikowana transakcja: {transaction_to_modify}")
        

    
def load_transaction_from_csv(filename: str, transactions) -> List[Transaction]:
    try:
        with open(filename, encoding='utf-8') as stream:
            content = csv.DictReader(stream)
            for row in content:
                trans_id = int(row["id"])
                description = row["description"]
                value = float(row["value"])
                if row["type"] == "Income":
                    transactions.append(Income(description, value))
                else:
                    transactions.append(Expense(description, value))
        print("\n Zaimportowano transakcje z pliku")
        print("Poniżej lista wszystkich transakcji")
        display_transactions(transactions)
    except FileNotFoundError:
        print("/n Plik nie istnieje. Nie zaimportowano żadnych danych.")

    return transactions


def save_transaction_to_csv(transactions: List[Transaction], filename: str = CSV_FILENAME) -> None:
    with open (filename, mode='w', newline='', encoding='utf-8') as stream:
        content = csv.writer(stream)
        content.writerow(['id', 'type', 'description', 'value'])

        for transaction in transactions:
            transaction_type = 'Income' if isinstance(transaction, Income) else 'Expense'
            content.writerow([transaction.id, transaction_type, transaction.description, transaction.value])

    print(f"\n Zapisano transakcje do pliku {filename}")

    



def main():
    transactions = []

    while True:
        menu_printing()
        try:
            user_choice = int(input("Wpisz odpowiednią cfrę: "))
        except ValueError:
            print("Błąd! Wpisz liczbę od 1 do 7")
            continue

        if user_choice == 1:
            new_transaction = Transaction.from_user_input()
            transactions.append(new_transaction)
            print(transactions)

        elif user_choice == 2:
            deleting_transaction(transactions)

        elif user_choice == 3:
            display_transactions(transactions)

        elif user_choice == 4:
            modifying_transaction(transactions)

        elif user_choice == 5:
            transactions = load_transaction_from_csv(CSV_FILENAME, transactions)
            

        elif user_choice == 6:
            save_transaction_to_csv(transactions)
  
        
        elif user_choice == 7:
            break


if __name__ == '__main__':
    main()