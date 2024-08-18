from fastapi import FastAPI
from server.router_hotel import router as router_hotel
from server.router_poi import router as router_poi

app = FastAPI()

app.include_router(router_hotel)
app.include_router(router_poi)