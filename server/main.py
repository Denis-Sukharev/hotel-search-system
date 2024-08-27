from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import uvicorn

from router_hotel import router as router_hotel
from router_poi import router as router_poi

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # HTTPSRedirectMiddleware,
    allow_origins=["http://localhost:5173/", "http://127.0.0.1:5173/", "http://172.17.3.34:8080/"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=[
        # "Cookie",
        "Content-Type",
        # "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
        "Credentials",
        "X-Requested-With",
        ],
)

app.include_router(
    router_hotel,
    prefix="/api",
)
app.include_router(
    router_poi,
    prefix="/api",
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)