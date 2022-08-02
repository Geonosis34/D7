from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import PostCategory, Category


@receiver(post_save, sender=PostCategory)
def send_sub_mail(sender, instance, created, **kwargs):

    global subscriber
    sub_text = instance.text
    category = Category.objects.get(pk=PostCategory.objects.get(pk=instance.pk).category.pk)
    print()
    print('category:', category)
    print()
    subscribers = category.subscribers.all()

    post = instance

    # для удобства вывода инфы в консоль, никакой важной функции не несет
    print('Адреса рассылки:')
    for qaz in subscribers:
        print(qaz.email)

    for subscriber in subscribers:
        print('Адресат:', subscriber.email)

        html_content = render_to_string(
            'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': post})

        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
            from_email='shishkin.vlad92@yandex.ru',
            to=[subscriber.email]
        )

        msg.attach_alternative(html_content, 'text/html')

        msg.send()

    return redirect('/news/')