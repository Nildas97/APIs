# importing libraries
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from sqlalchemy.orm import Session
from app.database import engine, get_db
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# connecting to postgresql
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='admin123',
            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successfull")
        break

    except Exception as error:
        print('Connecting to database failed')
        print("Error :", error)
        time.sleep(2)

# note
# install and open POSTMAN for API testing
# ----------------------------------------------------------------------------------------------------
# testing with ORM i.e. sqlalchemy


# fetching rows
@app.get("/sqlalchemy", response_model=List[schemas.PostResponse])
def get_rows(db: Session = Depends(get_db)):
    # get all rows
    post = db.query(models.Post).all()
    return post


# creating rows normal method
@app.post("/sqlalchemy", status_code=status.HTTP_201_CREATED)
def create_row(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # create rows
    new_post = models.Post(
        title=post.title, content=post.content, published=post.published)
    # add the rows
    db.add(new_post)
    # commit the rows
    db.commit()
    # retrieve the newly rows
    db.refresh(new_post)
    return {'data': new_post}


# creating rows cleaner method
@app.post("/sqlalchemy", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_rows(post: schemas.PostCreate, db: Session = Depends(get_db)):

    # create rows
    # print converted dict rows
    # print(**post.model_dump())

    # unpack automatically created dict rows
    new_post = models.Post(**post.model_dump())
    # add the rows
    db.add(new_post)
    # commit the rows
    db.commit()
    # retrieve the newly rows
    db.refresh(new_post)
    return new_post


# fetching post with id
@app.get("/sqlalchemy/{id}", response_model=schemas.PostResponse)
def fetch_post(id: int, db: Session = Depends(get_db)):
    # fetching one post
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return post


# delete post with id
@app.delete("/sqlalchemy/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # deleting one post
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    # if they didn't find post
    if deleted_post.first() is None:
        # raise 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exists")

    # if they find the post
    deleted_post.delete(synchronize_session=False)

    # commit
    db.commit()

    # display post deleted
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update single post
@app.put("/sqlalchemy/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # updating one post using sql in python
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    # if the post is not available
    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exists")

    # if post is available
    updated_post.update(post.model_dump(),
                        synchronize_session=False)

    # commit to push changes
    db.commit()

    # return the
    return updated_post.first()


# working with creating new database table
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # unpack automatically created dict rows
    new_user = models.User(**user.model_dump())
    # add the rows
    db.add(new_user)
    # commit the rows
    db.commit()
    # retrieve the newly rows
    db.refresh(new_user)
    return new_user
