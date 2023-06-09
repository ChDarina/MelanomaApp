import logging
from typing import List

from db.article import Article
from schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse
from sqlalchemy.orm import Session

from db.doctor import Doctor

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


def read_article(db: Session, article_id: int) -> ArticleResponse:
    db_article: Article = db.query(Article).filter(Article.id == article_id).first()
    if db_article is None:
        raise ValueError(f"Article not found with id {article_id}")
    doctor = db.query(Doctor).filter(Doctor.id == db_article.doctor_id).first()
    return ArticleResponse(id=db_article.id,
                           doctor_id=db_article.doctor_id,
                           doctor_name=doctor.name,
                           work_years=doctor.work_years,
                           title=db_article.title,
                           content=db_article.content,
                           datetime_created=db_article.datetime_created)


def read_articles(db: Session) -> List[ArticleResponse]:
    db_articles = db.query(Article).all()
    response: List[ArticleResponse] = []
    for db_article in db_articles:
        doctor = db.query(Doctor).filter(Doctor.id == db_article.doctor_id).first()
        response.append(ArticleResponse(id=db_article.id,
                                        doctor_id=db_article.doctor_id,
                                        doctor_name=doctor.name,
                                        work_years=doctor.work_years,
                                        title=db_article.title,
                                        content=db_article.content,
                                        datetime_created=db_article.datetime_created))
    return response


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
