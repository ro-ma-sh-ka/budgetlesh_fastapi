from fastapi import FastAPI
from . import models
from .database import engine
from .routers import expense, user, auth, currency, section

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# we use include_router to include path operations from different files after divided them
app.include_router(expense.router)
app.include_router(currency.router)
app.include_router(section.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello to web"}
