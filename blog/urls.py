from django.conf.urls import url
from . import views

# a标签：需要创建URL的时候，把必要的参数传递进去
# URLconf：配置一个URL方式，如果有参数，需要指定参数的正则类型，比如(?P<pk>[0-9])，这个就是说明，这里会有一个pk的参数被传递给view，并且这个参数的类型是至少有一位的数字
# view 可以在接收请求的时候，同时也获取这个参数



urlpatterns = [
    url(r'^$',views.post_list,name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),

]

