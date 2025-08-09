from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "posts"

    def ready(self):
        import posts.signals
        from watson import search as watson
        Post = self.get_model('Post')
        watson.register(Post, fields=('content',), search_engine="default")