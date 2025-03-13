from typing import List, Optional

CSV_FILENAME = 'wydatki.csv'

class Transaction:
    next_id = 1

    def __init__(self, description: str, value: float):
        self.id = Transaction.next_id  
        Transaction.next_id += 1  
        self.description = description
        self.value = value


    def __str__(self):
        return f"{self.id}. {self.value} | {self.description} " 
    

    def __repr__(self):
        return f"{self.__class__.__name__}id={self.id!r}, description={self.description!r}, value={self.value!r})"
    

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
        print("Brak zapisanych transakcji do wyświetlenia")
        return
    
    incomes = [t for t in transactions if isinstance (t, Income)]
    expenses = [t for t in transactions if isinstance(t, Expense)]

    print("\n PRZYCHODY:")
    if incomes:
        for income in incomes:
            print(income)

    else:
        print("Brak przychodów")

    print("\n WYDATKI:")
    if expenses:
        for expense in expenses:
            print(expense)
    else:
        print("Brak wydatków")
                

    
def file_opener(filename: str):
    try:
        with open(filename, encoding='utf-8') as stream:
            content = stream.read()
    except FileNotFoundError:
        print('File not found')
    
    return content


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

   

        elif user_choice == 3:
            display_transactions(transactions)

            
        
        elif user_choice == 7:
            break

    

if __name__ == '__main__':
    main()