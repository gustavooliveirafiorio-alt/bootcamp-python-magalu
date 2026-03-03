from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI(title="Async Banking API", description="Gerenciamento de depósitos e saques")

# Simulação de banco de dados em memória
fake_db = {
    "joao_silva": {"balance": 1000.0, "transactions": []}
}

@app.post("/transactions/", response_model=Transaction)
async def create_transaction(
    tx_data: TransactionCreate, 
    current_user: str = Depends(get_current_user)
):
    user_account = fake_db.get(current_user)
    
    # Validação de Saldo para Saques
    if tx_data.type == TransactionType.WITHDRAWAL:
        if user_account["balance"] < tx_data.amount:
            raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar o saque.")
        user_account["balance"] -= tx_data.amount
    else:
        user_account["balance"] += tx_data.amount

    # Registro da Transação
    new_tx = {
        "id": len(user_account["transactions"]) + 1,
        "timestamp": datetime.now(),
        **tx_data.model_dump()
    }
    user_account["transactions"].append(new_tx)
    return new_tx

@app.get("/statement/", response_model=List[Transaction])
async def get_statement(current_user: str = Depends(get_current_user)):
    return fake_db[current_user]["transactions"]
