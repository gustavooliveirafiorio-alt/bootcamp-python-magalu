from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn

app = FastAPI(title="Async Bank API", version="1.0.0")

# Simulação de Banco de Dados (In-memory para o exemplo)
db_accounts = {
    "user123": {"balance": 1000.0, "transactions": []}
}

# --- Endpoints ---

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Aqui entraria a lógica de verificação de senha
    return {"access_token": form_data.username, "token_type": "bearer"}

@app.post("/transactions/deposit", response_model=Transaction)
async def deposit(transaction: TransactionCreate, user: str = Depends(get_current_user)):
    if transaction.type != "deposit":
        raise HTTPException(status_code=400, detail="Tipo de transação inválido")
    
    # Lógica assíncrona de atualização
    db_accounts[user]["balance"] += transaction.amount
    new_tx = {**transaction.dict(), "id": len(db_accounts[user]["transactions"]) + 1, "timestamp": datetime.now()}
    db_accounts[user]["transactions"].append(new_tx)
    
    return new_tx

@app.post("/transactions/withdraw", response_model=Transaction)
async def withdraw(transaction: TransactionCreate, user: str = Depends(get_current_user)):
    current_balance = db_accounts[user]["balance"]
    
    if transaction.amount > current_balance:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")
    
    db_accounts[user]["balance"] -= transaction.amount
    # Registro da transação...
    return ...

@app.get("/statement", response_model=List[Transaction])
async def get_statement(user: str = Depends(get_current_user)):
    return db_accounts[user]["transactions"]
