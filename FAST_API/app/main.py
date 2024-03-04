# importing
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


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


# data_set
my_posts = [{"title": "somethings title", "content": "something content", "id": 1}, {
    "title": "favourite foods", "content": "sambhar", "id": 2}]


# function to find posts
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


# function to find index of post
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# to test get method
# @app.get("/posts")
# async def user():
#     return {"message": "Welcome to my APIs"}

# to test post method
# @app.post("/posts")
# def send_post(payload: dict = Body(...)):
#     print(payload)
#     return {'new_post': f"title {payload['title']} : content {payload['content']}"}

# to test schema validation
# @app.post("/posts")
# def make_post1(new_post: Post):
#     print(new_post.title)
#     return {"data": "new post"}

# to test published schema
# @app.post("/posts")
# def make_post2(new_post: Post):
#     print(new_post.published)
#     return {"data": "new post"}

# to test rating schema
# @app.post("/posts")
# def make_post3(new_post: Post):
#     print(new_post.rating)
#     return {"data": "new post"}

# to test the pydantic model as dict format
# @app.post("/posts")
# def make_post4(new_post: Post):
#     print(new_post)
#     print(new_post.model_dump())
#     return {"data": new_post}


# fetching the data created in the my_posts variable
@app.get("/posts")
def get_posts():
    # retrieve posts using sql in python
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {'Data': posts}


# sending the data just created
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # create posts using sql in python
    cursor.execute(
        """INSERT INTO posts (id, title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}


# sending the data just created
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post: Post):
#     # print(post.model_dump())

#     # after converting the array into dict
#     post_dict = post.model_dump()

#     # setting a random range for ids
#     post_dict['id'] = randrange(0, 1000000)

#     # first validating then appending as dictionary
#     my_posts.append(post_dict)
#     return {'data': post_dict}

# get a single post
# @app.get("/posts/{id}")
# def get_post(id):
#     print(id)
#     return {"post_detail": f"here is post {id}"}


# getting the latest post
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    print(post)
    return {"details": post}


# getting id along with title and content
# @app.get("/posts/{id}")
# def get_pozt(id: int):
#     post = find_post(id)
#     return {"post_detail": post}

# Change Response Status Code
# @app.get("/posts/{id}")
# def get_pozt(id: int, response: Response):
#     post = find_post(id)
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {f"{status.HTTP_404_NOT_FOUND} error : post with id {id} not found"}
#     return {"post_detail": post}

# Change Response Status Code
@app.get("/posts/{id}")
def get_pozt(id: int):
    # fetching one post using sql in python
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    return {"post_detail": post}


# note
# always keep in mind that path order matters.
# if you see above that get_pozt and get_latest_post
# both having same url path, just the id and latest are different
# but the fastapi couldn't recognize which one is which.

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

    # if they find, delete index
    # my_posts.pop(index)

    # display post deleted
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# # delete single post
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     # storing the post with id in index
#     index = find_index_post(id)
#     # if they didn't find index
#     if index is None:
#         # raise 404 error
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id : {id} does not exists")

#     # if they find, delete index
#     my_posts.pop(index)

#     # display post deleted
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# update single post
# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     # searches the index
#     index = find_index_post(id)
#     # if index not exist return 404 error
#     if index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id : {id} does not exists")

#     # if it exists convert to dictionary
#     post_dict = post.model_dump()

#     # add the id
#     post_dict['id'] = id

#     # post with index going to replace with post_dict
#     my_posts[index] = post_dict

#     # displays dictionary
#     return {"data": post_dict}


# update single post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # updating one post using sql in python
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} does not exists")

    return {"data": updated_post}
