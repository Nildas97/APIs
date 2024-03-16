# importing libraries
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from app.database import engine
from . import models
from dotenv import load_dotenv
import os



# getting current root directory
ROOT_DIR = os.getcwd()

# getting the .env folder path
ENV_FILE_PATH = os.path.join(ROOT_DIR, '.env')

# loading the .env file
load_dotenv(dotenv_path=ENV_FILE_PATH)

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# class for setting basic structure of data
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# connecting to postgresql
while True:
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user=os.getenv('USERNAME'),
            password=os.getenv('PASSWORD'),
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
# testing with Database i.e. Postgresql


# fetching the data created
@app.get("/posts")
def get_posts():
    # retrieve posts using sql in python
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {'Data': posts}


# sending the data just created
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostBase):
    # create posts using sql in python
    cursor.execute(
        """INSERT INTO posts (id, title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}


# fetching post
@app.get("/posts/{id}")
def get_pozt(id: int):
    # fetching one post using sql in python
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return {"post_detail": post}


# delete single post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting one post using sql in python
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    # if they didn't find index
    if deleted_post is None:
        # raise 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exists")

    # display post deleted
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update single post
@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate):
    # updating one post using sql in python
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exists")

    return {"data": updated_post}
