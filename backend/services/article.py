import logging
from typing import List

from db.article import Article
from schemas.article import ArticleCreate, ArticleUpdate
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def create_article(db: Session, article: ArticleCreate) -> Article:
    db_article = Article(
        doctor_id=article.doctor_id,
        title=article.title,
        content=article.content,
        datetime_created=article.datetime_created)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def read_article(db: Session, article_id: int) -> Article:
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article is None:
        raise ValueError(f"Article not found with id {article_id}")
    return db_article


def read_articles(db: Session) -> List[Article]:
    return db.query(Article).all()


def update_article(db: Session, article_id: int, article: ArticleUpdate) -> Article:
    db_article = read_article(db, article_id)
    for key, value in article.dict(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article


def delete_article(db: Session, article_id: int) -> None:
    db_article = read_article(db, article_id)
    db.delete(db_article)
    db.commit()
