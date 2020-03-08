#from django.conf.urls import url
from  django.urls import path
from . import views

urlpatterns = [
        path('', views.homepage,name="home" ),
        path('home', views.homepage,name="home2" ),
        path('lda', views.lda, name = "lda"),
        path('w2v', views.w2v, name = "w2v"),
        path('pattern', views.pattern, name = "pattern"),
#        url('pattern',views.pattern, name = "pattern"),
        ]
