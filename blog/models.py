from typing import Dict
from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

# Create your models here.

# class Image(models.Model):
#     """Image content support"""
#     image = models.ImageField(upload_to="imgs")
#     name = models.CharField(max_length=255)
#     def __str__(self):
#         return self.name

class Post(models.Model):
    """Post model"""
    title = models.CharField(max_length=200)
    content = models.TextField()  # Post content WYSIWYG
    updated = models.DateTimeField(auto_now=True)  # Last updated time
    excerpt = models.CharField(max_length=400, blank=True)
    tags = models.CharField(max_length=256, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=1024, blank=True)

def get_all_posts() -> Dict[int, Dict]:
    """Return all posts without content"""
    fields = {
        "title": lambda obj: obj,
        "excerpt": lambda obj: obj[0:200],
        "tags": lambda obj: obj.split(','),
        "image": lambda obj: obj,
        "updated": lambda obj: obj.strftime("%Y-%m-%d")
    }
    result: Dict[int, Dict] = dict()

    # pylint: disable=no-member
    for post in Post.objects.all():
        data = dict()
        for key, handler in fields.items():
            data[key] = handler(post.serializable_value(key))
        result[post.id] = data

    return result


def get_post(postid: int) -> Dict:
    """Get one specified post or 404"""
    fields = {
        "id": lambda obj: int(obj),
        "content": lambda obj: obj,
        "title": lambda obj: obj,
        "tags": lambda obj: obj.split(','),
        "image": lambda obj: obj,
        "updated": lambda obj: obj.strftime("%Y-%m-%d")
    }

    post = get_object_or_404(Post, pk=postid)
    result = dict()
    for key, handler in fields.items():
        result[key] = handler(post.serializable_value(key))
    return result

def new_post(postid: int, post: Dict) -> None:
    """Save / Create a new post"""
    try:
        # pylint: disable=no-member
        oldpost = Post.objects.get(pk=postid)
        oldpost.content = post.get("content", '')
        oldpost.title = post.get("title", oldpost.title)
        oldpost.tags = ','.join(post.get("tags", ''))
        oldpost.image = post.get("image", '')
        oldpost.excerpt = post.get("excerpt", '')
    except Post.DoesNotExist as _error:
        post["tags"] = ','.join(post.get("tags", ''))
        oldpost = Post(**post)
    oldpost.save()