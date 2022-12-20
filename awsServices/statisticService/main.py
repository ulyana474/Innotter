from fastapi import FastAPI
from statisticService.router import router

app = FastAPI()
app.include_router(router)
