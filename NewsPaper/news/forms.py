from django import forms
from django.forms import ModelForm, BooleanField, Textarea  # Импортируем true-false поле
from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Галочка!')  # добавляем галочку или же true-false поле

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['author.authorUser|title'].empty_label = "Автор не выбран"
        self.fields['author'].empty_label = "Автор не выбран"
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля.
    # Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'check_box']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 50, 'rows': 3}),
        }
