
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:postid>', views.post),
    path('posts', views.restful_posts),                  # Restful
    path('settings', views.restful_settings),            # Restful
    path('posts/<int:postid>', views.restful_posts),     # Restful
    path('dashboard/login', views.userlogin),
    path('dashboard/logout', views.userlogout),
    path('dashboard/posts', views.manage_posts),
    path('dashboard/settings', views.manage_settings)
]

# path('images/<int:imageid>', views.restful_images),  # Restful
# path('dashboard/images', views.manage_images),
