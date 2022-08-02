# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, View
from .models import News, Category
from datetime import datetime
from .filters import NewsFilter
from .forms import NewsForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives



class NewsList(ListView):
    model = News
    template_name = 'simpleapp/news.html'
    context_object_name = 'news'
    queryset = News.objects.order_by('-dateCreation')
    paginate_by = 2  # вот так мы можем указать количество записей на странице

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_upgrade'] = "Обновление каждый четверг"
        context['filterset'] = self.filterset
        return context

class NewsDetail(DetailView):
    model = News
    template_name = 'simpleapp/news_detail.html'
    context_object_name = 'news_detail'

# Подписка пользователя в категорию новостей
@login_required
def subscribe_to_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    is_subscribed = cat.subscribers.filter(id=user.id).exists()
    if not is_subscribed:
        cat.subscribers.add(user)
        html = render_to_string(  # передаем в шаблон переменные, тут передал категорию для вывода ее в письме
            template_name='simpleapp/subscribed_category.html',
            context={
                'categories': cat,
                'user': user,
            },
        )
        cat_repr = f'{cat}'
        email = user.email
        msg = EmailMultiAlternatives(
            subject=f'Subscription to {cat_repr} category',
            from_email='shishkin.vlad92@yandex.ru',
            to=[email, ],
        )

        msg.attach_alternative(html, 'text/html')
        try:
            msg.send()
        except Exception as e:
            print(e)

        return redirect('/news/')

    return redirect('/news/')

# Отписка пользователя от категории новостей
@login_required
def unsubscribe_from_category(request, pk):
    user = request.user
    cat = Category.objects.get(id=pk)
    is_subscribed = cat.subscribers.filter(id=user.id).exists()

    if is_subscribed:
        cat.subscribers.remove(user)
    return redirect('/news/')


class NewsCreate(PermissionRequiredMixin, CreateView):
    template_name = 'simpleapp/news_add.html'
    form_class = NewsForm
    context_object_name = 'news_create'
    model = News
    permission_required = ('news.news_add', )

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    model = News
    template_name = 'simpleapp/news_add.html'
    permission_required = ('news.news_update',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return News.objects.get(pk=id)

class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = News
    template_name = 'simpleapp/news_delete.html'
    success_url = '/news/'
    queryset = News.objects.all()
    permission_required = ('news.news_delete',)

class NewsSearch(ListView):
    model = News
    template_name = 'simpleapp/news_search.html'
    context_object_name = 'search'
    queryset = News.objects.order_by('-dateCreation')



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET,
                                          queryset=self.get_queryset())
        return context
