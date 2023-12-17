import pytest

from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
def test_news_count(client, some_news):
    url = reverse('news:home')
    response = client.get(url)
    assert len(
        response.context['object_list']
    ) == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, some_news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, some_comments, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.parametrize(
    'user_client, form_exists',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_pages_contains_form(user_client, form_exists, news):
    url = reverse('news:detail', args=(news.id,))
    response = user_client.get(url)
    assert form_exists == ('form' in response.context)
