from fastapi import FastAPI
from src.app.utils.cors import setup_cors
from src.app.db.database import create_db_and_tables
from src.app.utils.rate_limiter import setup_rate_limiter
from src.app.api.hero_routes import hero_router
from src.app.api.user_routes import user_router

app = FastAPI()

version = "v1"
setup_cors(app)
setup_rate_limiter(app)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(hero_router, prefix=f"/api/{version}", tags=["heroes"])
app.include_router(user_router, prefix=f"/api/{version}", tags=["users"])