from django.urls import reverse

def test_notification_url():
    url = reverse('notification:process-notification', args=[1])

    assert url == f'/{1}/process/'