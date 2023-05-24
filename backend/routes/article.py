import logging
from typing import List

from db.base import Base, engine, get_db
from fastapi import Depends, HTTPException, APIRouter
from schemas.article import ArticleModel, ArticleCreate, ArticleUpdate
from sqlalchemy.orm import Session
from starlette import status

from services.article import delete_article, update_article, read_article, read_articles, create_article

Base.metadata.create_all(engine)

router = APIRouter(prefix="/article",
                   tags=["articles"],
                   responses={404: {"description": "Articles router not found"}})

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


@router.post("/", response_model=ArticleModel)
def create_article_route(article: ArticleCreate, db: Session = Depends(get_db)):
    try:
        return create_article(db, article)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{article_id}", response_model=ArticleModel)
def get_article_route(article_id: int, db: Session = Depends(get_db)):
    try:
        return read_article(db, article_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[ArticleModel])
def get_companies_route(db: Session = Depends(get_db)):
    try:
        return read_articles(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{article_id}", response_model=ArticleModel)
def update_article_route(article_id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    try:
        return update_article(db, article_id, article)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{article_id}")
def delete_article_route(article_id: int, db: Session = Depends(get_db)):
    try:
        delete_article(db, article_id)
        return {"detail": f"Article with id {article_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
