from fastapi import FastAPI
from lecture_2.hw.shop_api.shop.routes import router


app = FastAPI(title="Shop API")
app.include_router(router)