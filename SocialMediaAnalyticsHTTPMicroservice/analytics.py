from fastapi import FastAPI, Query
import requests
import json
from collections import defaultdict

app = FastAPI()

BASE_URL = "http://20.244.56.144/test"
user_post_counts = {}
posts = []
post_comment_counts = {}

def fetch_and_cache_data():
    global user_post_counts, posts, post_comment_counts
    
    users = requests.get(f"{BASE_URL}/users").json()
    posts = requests.get(f"{BASE_URL}/posts").json()
    comments = requests.get(f"{BASE_URL}/comments").json()
    
    # store users and their post counts
    user_post_counts = defaultdict(int)
    for post in posts:
        user_post_counts[post["userId"]] += 1
    
    # store comments count per post
    post_comment_counts = defaultdict(int)
    for comment in comments:
        post_comment_counts[comment["postId"]] += 1

@app.get("/users")
def top_users():
    top_users = sorted(user_post_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    return [{"userId": user_id, "postCount": count} for user_id, count in top_users]

@app.get("/posts")
def top_or_latest_posts(type: str = Query("popular", regex="^(popular|latest)$")):
    if type == "popular":
        max_comments = max(post_comment_counts.values(), default=0)
        popular_posts = [post for post in posts if post_comment_counts.get(post["id"], 0) == max_comments]
        return popular_posts
    
    if type == "latest":
        latest_posts = sorted(posts, key=lambda x: x["timestamp"], reverse=True)[:5]
        return latest_posts

# fetch and cache data on startup
fetch_and_cache_data()