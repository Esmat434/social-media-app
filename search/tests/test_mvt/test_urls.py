from django.urls import reverse

class TestUrls:
    def test_post_search_url(self):
        url = reverse('post_search')+'?q=hi'

        assert url == '/search/post/?p=hi'