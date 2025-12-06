from fastapi import FastAPI
from .schemas import Expense

app = FastAPI()

expenses = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/expenses", response_model=list[Expense])
def get_expenses():
    return expenses

@app.post("/expenses", response_model=Expense)
def create_expense(expense: Expense):
    expenses.append(expense)
    return expense
