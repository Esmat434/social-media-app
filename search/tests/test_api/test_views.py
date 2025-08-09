import pytest
from django.urls import reverse

@pytest.mark.django_db
class TestSearchPostView:
    def test_get_method(self,client):
        url = reverse('api_search:post_search')+'?q=test'
        response = client.get(url)

        assert response.status_code == 200

@pytest.mark.django_db
class TestSearchUserView:
    def test_get_method(self,client):
        url = reverse('api_search:user_search')+'?q=test'
        response = client.get(url)

        assert response.status_code == 200