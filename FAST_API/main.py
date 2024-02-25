from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "somethings title", "content": "something content", "id": 1}, {
    "title": "favourite foods", "content": "sambhar", "id": 2}]


# @app.get("/posts")
# async def user():
#     return {"message": "Welcome to my APIs"}


# @app.post("/posts")
# def send_post(payload: dict = Body(...)):
#     print(payload)
#     return {'new_post': f"title {payload['title']} : content {payload['content']}"}


# @app.post("/posts")
# def make_post1(new_post: Post):
#     print(new_post.title)
#     return {"data": "new post"}


# @app.post("/posts")
# def make_post2(new_post: Post):
#     print(new_post.published)
#     return {"data": "new post"}


# @app.post("/posts")
# def make_post3(new_post: Post):
#     print(new_post.rating)
#     return {"data": "new post"}


# @app.post("/posts")
# def make_post4(new_post: Post):
#     print(new_post)
#     print(new_post.model_dump())
#     return {"data": new_post}

@app.get("/posts")
def get_posts():
    return {'Data': my_posts}


@app.post("/posts")
def create_post():
    return {'message': "post is initiated"}
