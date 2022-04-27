from fastapi import FastAPI 

from cookapps.routes import router
from cookapps.database import setup_database 


app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    await setup_database()
