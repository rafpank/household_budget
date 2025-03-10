from typing import List
import csv


class Expense:
    def __init__(self, id: int, description: str, value: float):
        self.id = id
        self.description = description
        self.value = value


    def __str__(self):
        return f"{self.id}. {self.value} | {self.description} " 
    

    def __repr__(self):
        return f"Expense(id={self.id!r}, description={self.description!r}, value={self.value!r})"
    


# def find_next_id(expenses: List[Expense]):
#     id = 




def main():
    print('Trutu tutu')



if __name__ == '__main__':
    main()