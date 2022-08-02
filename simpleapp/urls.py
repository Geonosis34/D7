from django.urls import path, include
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, NewsSearch, subscribe_to_category, unsubscribe_from_category


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', NewsList.as_view()),
   path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('search/', NewsSearch.as_view(), name='news_search'),
   path('subscribe/<int:pk>', subscribe_to_category, name='sub_cat'),
   path('unsubscribe/<int:pk>', unsubscribe_from_category, name='unsub_cat'),
]