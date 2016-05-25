"""TweetBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from homepage import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^get_tweets/$', views.get_tweets, name='index'),
    url(r'^get_by_genre/$', views.get_by_genre, name='get_by_genre'),
    url(r'^get_genres/$', views.get_genres, name='get_genres'),
    url(r'^get_ranked/$', views.get_ranked, name='get_ranked'),
    url(r'^get_sentiment_breakdown/$', views.get_sentiment_breakdown, name='get_sentiment_breakdown'),
    url(r'^get_sentiment_trends/$', views.get_sentiment_trends, name='get_sentiment_trends'),
    url(r'^get_info/$', views.get_info, name='get_info'),
    url(r'^get_tweets_for_map/$', views.get_tweets_for_map, name='get_tweets'),
    url(r'^get_data/$', views.get_data, name='get_data'),
    url(r'^get_username/$', views.get_username, name='get_username'),
    url(r'^get_top/$', views.get_top, name='get_top'),
    url(r'^get_tweets_distance/$', views.get_tweets_distance, name='index'),
    url(r'^register_user/$', views.add_user, name='add_user'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^test_user/$', views.test_user, name='test_user'),
]
