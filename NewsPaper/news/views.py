from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.core.paginator import Paginator
from .models import Post, Category, Author, PostCategory, Comment
from .filters import PostFilter
from .forms import PostForm

from django.http.response import HttpResponse
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class News(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-dateCreation']
    form_class = PostForm
    paginate_by = 10  # постраничный вывод в 1элемент

    def get_queryset(self):
        queryset = PostFilter(self.request.GET, super().get_queryset()).qs
        # фильтрация queryset-ом
        return queryset


    def get_context_data(self, **kwargs):  # забираем отфильтрованные
        # объекты переопределяя метод get_context_data у
        # наследуемого класса - полиморфизм
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        # context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        # берём значения для нового товара из POST-запроса отправленного на сервер
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)

    # def get(self, request):
    #     news = Post.objects.order_by('-dateCreation')
    #     p = Paginator(news, 3)  # объект класса пагинатор- передаём ему список товаров c количество для одной стр
    #     news = p.get_page(request.GET.get('page', 1))  # N стр из get-запроса. Если ничего не передали,
    #     # будем показывать первую страницу.
    #     # теперь вместо всех объектов в списке товаров хранится только нужная нам страница с товарами
    #     data = {
    #         'news': news,
    #     }
    #     return render(request, 'news.html', data)


# создаём представление, в котором будут детали конкретного отдельного товара
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'news/post_detail.html'  # название шаблона будет product.html
    queryset = Post.objects.all()
    context_object_name = 'post'  # название объекта

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)

        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


    def post_list_view(request):
        paginator = Paginator(News.objects.all(), per_page=3)
        page = paginator.page(request.GET.get('page', 1))
        return render(request, 'news/news.html', {
            'object_list': page.object_list,
            'page_obj': page,
        })


#  ++ дженерик для создания объекта. Надо указать только имя шаблона и класс формы который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/post_create0.html'
    form_class = PostForm
    context_object_name = 'news'
    permission_required = ('news.add_post',)


# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news/post_edit.html'
    form_class = PostForm
    context_object_name = 'news'
    permission_required = ('news.change_post',)


    # class ProtectedView(LoginRequiredMixin, TemplateView):
    #     template_name = 'news/post_edit.html'  # 'protected_page.html'

    # метод get_object вместо queryset для получения инфо об obj редактирования
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    # class MyView(LoginRequiredMixin, TemplateView):
    #     login_url = '/login/'
    #     redirect_field_name = 'news/post_edit.html'

# дженерик для удаления товара
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'news/ post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news'
    permission_required = ('news.delete_post',)


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для поиска поста
class Search(ListView):
    model = Post
    template_name = 'news/search2.html'
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = [
        '-dateCreation']  # сортировка по дате публикации, сначала более новые /  queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10

    def get_queryset(self):
        queryset = PostFilter(self.request.GET, super().get_queryset()).qs
        # фильтрация queryset-ом
        return queryset

    def get_context_data(self, **kwargs):
        # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['form'] = PostForm()
        return context
