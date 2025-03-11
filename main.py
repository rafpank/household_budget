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

    
def file_opener(filename: str):
    try:
        with open(filename, encoding='utf-8') as stream:
            content = stream.read()
    except FileNotFoundError:
        print('File not found')
    
    return content


def creating_transaction() -> Transaction | str:
    while True:
        description = input("Podaj opis: ").strip()
        if not description:
            print("Błąd! Opis nie może być pusty.")
            continue
        try:
            value = int(input("Podaj wartość: ").strip())
            if value <= 0:
                print("Błąd! Wartość musi być większa od 0.")
                continue
        except ValueError:
            print("Błąd! Wartość musi być liczbą.")
            continue
            
        indicator_incom_or_expense = input("Określ czy to jest przychód czy wydatek? [p/w]: ").lower()
        
        if indicator_incom_or_expense == 'p':
            return Income(description, value)
        elif indicator_incom_or_expense == 'w':
            return Expense(description, value)
        else:
            return "Błąd! Wybierz 'p' dla przychodu lub 'w' dla wydatku."




def main():
    transactions = []

    while True:
        menu_printing()
        try:
            user_choice = int(input("Wpisz odpowiednią cfrę: "))
        except ValueError:
            print("Błąd! Wpisz liczbę od 1 do 7")

        if user_choice == 1:
            new_transaction = creating_transaction()
            if isinstance(new_transaction, Transaction):
                transactions.append(new_transaction)
                print(transactions)
            else:
                print("Niewłaściw wybór")
        
        elif user_choice == 7:
            break

    

if __name__ == '__main__':
    main()