import logging

from fastapi import FastAPI

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

app = FastAPI()


@app.get("/")
async def root():
    logging.info("Root application start")
