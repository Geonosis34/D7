from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings
from .models import News
from datetime import timedelta, date
from time import sleep

from celery import shared_task



def collect_subscribers(category):
    """
    iterate thro all subscribers in Category table, extract their email and form up a list of email recepients
    """
    email_recipients = []
    for user in category.subscribers.all():
        email_recipients.append(user.email)
    print(f'collect_subscribers func: {email_recipients}')
    return email_recipients


def send_emails(post_object, *args, **kwargs):
    # print(kwargs['template'])
    html = render_to_string(
        kwargs['template'],
        {'category_object': kwargs['category_object'], 'post_object': post_object},
        # передаем в шаблон любые переменные
    )
    print(kwargs)
    msg = EmailMultiAlternatives(
        subject=kwargs['email_subject'],
        from_email=settings.EMAIL_HOST_USER,
        to=kwargs['email_recipients']  # отправляем всем из списка
    )
    msg.attach_alternative(html, 'text/html')
    msg.send(fail_silently=False)


@shared_task
def new_post_subscription(oid):
    template = 'simpleapp/news.html'
    latest_pst = News.objects.get(pk=oid)
    # print(latest_post)
    # print(f'latest_post.isUpdated = {latest_post.isUpdated}')

    # if not latest_pst.isUpdated:
    # sleep(5)
    print(latest_pst.title)
    categories = latest_pst.cats.all()
    print(f'categories = {categories}')
    for category in categories:
        # print('do we get into for?')
        email_subject = f"News in Category: '{category}'"
        print(f'category = {category}')
        email_recipients = collect_subscribers(category)
        print(f'new_post_subscription func collected subscribers: {email_recipients}')
        send_emails(
            latest_pst,
            category_object=category,
            email_subject=email_subject,
            template=template,
            email_recipients=email_recipients)


@shared_task
def notify_subscribers_weekly():
    week = timedelta(days=7)
    posts = News.objects.all()
    past_week_posts = []
    template = 'simpleapp/weekly_digest.html'
    email_subject = 'Your News Portal Weekly Digest'

    for news in posts:
        time_delta = date.today() - news.time_pub.date()
        if time_delta < week:
            past_week_posts.append(news)

    past_week_categories = set()
    for news in past_week_posts:

        for category in news.cats.all():
            past_week_categories.add(category)

    print(f'past_week_categories = {past_week_categories}')

    email_recipients_set = set()
    for category in past_week_categories:
        print(f'category.subscribers.all = {category.subscribers.all()}')
        # email_subject = f'New post in category: "{category}"'
        get_user_emails = set(collect_subscribers(category))
        email_recipients_set.update(get_user_emails)
        print(f'get_user_emails = {get_user_emails}')
    email_recipients = list(email_recipients_set)
    print(email_recipients)

    for email in email_recipients:
        post_object = []
        categories = set()

        for news in past_week_posts:
            subscription = news.cats.all().values('subscribers').filter(subscribers__email=email)

            if subscription.exists():
                print(f'subscription = {subscription}')
                post_object.append(news)
                categories.update(news.cats.filter(subscribers__email=email))
        print(f'email = {email}')
        print(f'post_object = {post_object}')
        category_object = list(categories)
        print(f'category_object = {category_object}')
        print(f'set(news.cats.all()) = {set(news.cats.all())}')

        send_emails(
            post_object,
            category_object=category_object,
            email_subject=email_subject,
            template=template,
            email_recipients=[email, ]
        )