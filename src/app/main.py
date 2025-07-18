from fastapi import FastAPI
from src.app.db.database import create_db_and_tables
from src.app.utils.rate_limiter import setup_rate_limiter
from src.app.api.routes import router

app = FastAPI()

version = "v1"

setup_rate_limiter(app)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(router, prefix=f"/api/{version}", tags=["heroes"])