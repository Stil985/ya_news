import pytest
from pytest_django.asserts import assertFormError
from django.urls import reverse

from news.models import Comment
from news.forms import WARNING


def test_anonymous_client_cant_create_comment(client, form_data, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.post(url, data=form_data)
    assert response.status_code == 302
    assert Comment.objects.count() == 0


def test_user_can_create_comment(author_client, form_data, news, author):
    url = reverse('news:detail', args=(news.id,))
    author_client.post(url, data=form_data)
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author
    assert Comment.objects.count() == 1


def test_user_cant_use_bad_words(author_client, bad_form_data, news):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=bad_form_data)
    assertFormError(response, 'form', 'text', WARNING)
    assert Comment.objects.count() == 0


@pytest.mark.parametrize(
    'parametrized_client, is_equal',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('admin_client'), False),
    )
)
def test_user_can_edit_comment(
    parametrized_client,
    is_equal,
    comment,
    form_data
):
    url = reverse('news:edit', args=(comment.pk,))
    parametrized_client.post(url, data=form_data)
    edited_comment = Comment.objects.get()
    assert (
        edited_comment.text == form_data['text']
    ) == is_equal


@pytest.mark.parametrize(
    'parametrized_client, comment_count',
    (
        (pytest.lazy_fixture('author_client'), 0),
        (pytest.lazy_fixture('admin_client'), 1),
    )
)
def test_user_can_edit_comment(
    parametrized_client,
    comment_count,
    comment,
    form_data
):
    url = reverse('news:delete', args=(comment.pk,))
    parametrized_client.post(url, data=form_data)
    assert Comment.objects.count() == comment_count
