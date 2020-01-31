from django.urls import path,re_path
# 导入 myapp 应用的 views 文件
from . import views
# from django.conf.urls import url, include
# from myapp.views import add_book,show_books
# add_book

urlpatterns = [
    re_path(r'add_book$', views.add_book),
    re_path(r'show_books$', views.show_books)
]