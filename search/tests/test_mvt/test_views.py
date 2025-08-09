from django.urls import reverse
import pytest

@pytest.mark.django_db
class TestSearchPostView:
    def test_get_method(self,client):
        url = reverse('mvt_search:post_search')+'?q=hello'
        response = client.get(url)

        assert response.status_code == 200