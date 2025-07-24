from django.urls import reverse

class TestUrls:
    def test_create_post_url(self):
        url = reverse('api_posts:post_create')

        assert url == '/api/post/create/'
    
    def test_post_delete_or_update_url(self):
        url = reverse('api_posts:post_delete_or_update', args=[1])

        assert url == f'/api/post/{1}/'
    
    def test_comment_create_url(self):
        url = reverse('api_posts:comment_create')

        assert url == f'/api/comment/create/'
    
    def test_comment_delete_or_update_url(self):
        url = reverse('api_posts:comment_delete_or_update', args=[1])

        assert url == f'/api/comment/{1}/'

    def test_like_create_url(self):
        url = reverse('api_posts:like_create')

        assert url == '/api/like/create/'
    
    def test_like_delete(self):
        url = reverse('api_posts:like_delete', args=[1])

        assert url == f'/api/like/{1}/'
    
    def test_share_create(self):
        url = reverse('api_posts:share_create')

        assert url == '/api/share/create/'
    
    def test_share_delete_url(self):
        url = reverse('api_posts:share_delete', args=[1])

        assert url == f'/api/share/{1}/'
    
    def test_save_create_url(self):
        url = reverse('api_posts:save_create')

        assert url == '/api/save/create/'
    
    def test_save_delete_url(self):
        url = reverse('api_posts:save_delete', args=[1])

        assert url == f'/api/save/{1}/'
    