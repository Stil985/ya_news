import pytest
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news(author):
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def id_for_news(news):
    return news.pk,


@pytest.fixture
def id_for_comment(comment):
    return comment.pk,


@pytest.fixture
def some_news():
    today = datetime.today()
    return News.objects.bulk_create([
        News(
            title=f'Заголовок {i}',
            text=f'Текст {i}',
            date=today - timedelta(days=i)
        )
        for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ])


@pytest.fixture
def some_comments(news, author):
    now = timezone.now()
    return Comment.objects.bulk_create([
        Comment(
            news=news,
            author=author,
            text=f'Текст комментария {i}',
            created=now - timedelta(days=i)
        )
        for i in range(2)
    ])
