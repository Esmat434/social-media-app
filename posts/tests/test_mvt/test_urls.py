from django.urls import reverse

class TestUrls:
    def test_create_post_url(self):
        url = reverse('mvt_posts:create_post')

        assert url == '/post/create/'
    
    def test_edit_post_url(self):
        url = reverse('mvt_posts:edit_post', args=[1])

        assert url == f'/post/{1}/edit/'
    
    def test_delete_post_url(self):
        url = reverse('mvt_posts:delete_post', args=[1])

        assert url == f'/post/{1}/delete/'
    
    def test_create_comment_url(self):
        url = reverse('mvt_posts:create_comment', args=[1])

        assert url == f'/comment/{1}/create/'
    
    def test_create_parent_comment_url(self):
        url = reverse('mvt_posts:create_parent_comment', args=[1,1])

        assert url == f'/parent_comment/{1}/{1}/create/'
    
    def test_edit_comment_url(self):
        url = reverse('mvt_posts:edit_comment', args=[1])

        assert url == f'/comment/{1}/edit/'
    
    def test_delete_comment_url(self):
        url = reverse('mvt_posts:delete_comment', args=[1])

        assert url == f'/comment/{1}/delete/'
    
    def test_create_like_url(self):
        url = reverse('mvt_posts:create_like', args=[1])

        assert url == f'/like/{1}/create/'
    
    def test_create_share_url(self):
        url = reverse('mvt_posts:create_share', args=[1])

        assert url == f'/share/{1}/create/'
    
    def test_create_save_url(self):
        url = reverse('mvt_posts:create_save', args=[1])

        assert url == f'/save/{1}/create/'