import pytest

from django.urls import reverse
from django.conf import settings

class TestMaintenanceModeMiddleware:
    
    @pytest.fixture(autouse=True)
    def setUp(self,client):
        self.client = client
    
    def test_maintenance_mode_middleware(self):
        settings.MAINTENANCE_MODE = True
        url = reverse('api:profile', args=[1])
        response = self.client.get(url)

        assert response.status_code == 200
        assert 'accounts/maintenance.html' in [t.name for t in response.templates]
