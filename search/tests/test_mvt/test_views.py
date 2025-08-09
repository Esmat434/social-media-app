from django.urls import reverse
import pytest

@pytest.mark.django_db
class TestSearchPostView:
    def test_get_method(self,client):
        url = reverse('mvt_search:post_search')+'?q=hello'
        response = client.get(url)

        assert response.status_code == 200

@pytest.mark.django_db
class TestSearchNetworkView:
    def test_get_method(self,client):
        url =  reverse('mvt_search:network_search')+'?q=jan'
        response = client.get(url)

        assert response.status_code == 200

@pytest.mark.django_db
class TestSearchNotificationView:
    def test_get_method(self,client):
        url = reverse('mvt_search:notification_search')+'?q=liked'
        response = client.get(url)

        assert response.status_code == 200