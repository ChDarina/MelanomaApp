import logging

from fastapi import FastAPI

from routes import company, photo

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

app = FastAPI()
app.include_router(company.router)
app.include_router(photo.router)


@app.get("/")
async def root():
    logging.info("Root application start")
