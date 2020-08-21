import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .manager import JSONSettingsManager
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotAllowed
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post, get_all_posts
from .models import get_post
from .models import new_post

# Create your views here.
manager = JSONSettingsManager("config.json")


def index(request):  # Done
    return render(request, "index.html", context={
        "title": manager.current["title"],
        "subtitle": manager.current["subtitle"],
        "menus": json.dumps(manager.current["menus"], ensure_ascii=False),
        "posts": json.dumps(get_all_posts(), ensure_ascii=False)
    })


def post(request, postid):  # Done
    return render(request, "post.html", context={
        "title": manager.current["title"],
        "subtitle": manager.current["subtitle"],
        "menus": json.dumps(manager.current["menus"], ensure_ascii=False),
        "post": json.dumps(get_post(postid), ensure_ascii=False)
    })


@login_required
def restful_settings(request):  # Done
    if request.method == "POST":
        settings = json.loads(request.body.decode())
        manager.write(settings)
        return HttpResponse('')
    return HttpResponseNotAllowed(["POST"])


# @login_required
# def restful_images(request, imgid):
#     if request.method == "POST":
#         pass
#     if request.method == "DELETE":
#         pass
#     return HttpResponseNotAllowed(["POST", "DELETE"])


# @login_required
# def manage_images(request):
#     return render(request, "post.dashboard.html", context={
#         "title": manager.current["title"]
#     })


@login_required
@csrf_exempt
def restful_posts(request, postid):  # Done
    if request.method == "POST":
        post = json.loads(request.body.decode())["post"]
        post["author"] = request.user
        new_post(postid, post)
        return HttpResponse('')
    if request.method == "GET":
        return HttpResponse(json.dumps(get_post(postid), ensure_ascii=False))
    if request.method == "DELETE":
        post = get_object_or_404(Post, pk=postid)
        post.delete()
        return HttpResponse('')
    return HttpResponseNotAllowed(["GET", "POST", "DELETE"])


def userlogin(request):  # Done
    if request.method == "POST":
        data = json.loads(request.body.decode())
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("/dashboard/posts")
        else:
            return HttpResponseForbidden()
    if request.method == "GET":
        return render(request, "login.html")


def userlogout(request):  # Done
    logout(request)
    return redirect("/")


@login_required
def manage_posts(request):  # Done
    return render(request, "post.dashboard.html", context={
        "title": manager.current["title"],
        "posts": json.dumps(get_all_posts(), ensure_ascii=False)
    })


@login_required
def manage_settings(request):  # Done
    return render(request, "setting.dashboard.html", context={
        "title": manager.current["title"],
        "subtitle": manager.current["subtitle"],
        "menus": json.dumps(manager.current["menus"], ensure_ascii=False),
    })
