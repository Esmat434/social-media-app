import pytest

from django.contrib.auth import get_user_model

from connections.models import Connection
from connections.algorithms.FriendsConnections import shared_connections_suggestion

User = get_user_model()

@pytest.mark.django_db
class TestFriendsConnectionsAlgorithms:
    @pytest.fixture(autouse=True)
    def setUp(self):
        user_name = ['user1','user2','user3','user4','user5','user6','user7','user8','user9','user10']
        for name in user_name:
            User.objects.create_user(
                username=name,
                email=f'{name}@gmail.com',
                address='test1',
                city='test1',
                country='AF'
            )

        self.user = User.objects.get(username='user1')
        for name in user_name[1:]:
            from_user = User.objects.get(username=name)
            Connection.objects.create(
                from_user=from_user, 
                to_user=self.user, 
                status=Connection.ConnectionStatus.ACCEPTED
            )
            Connection.objects.create(
                from_user=self.user, 
                to_user=from_user, 
                status=Connection.ConnectionStatus.ACCEPTED
            )

    def test_shared_connections_suggestion(self):
        ranked_suggestion = shared_connections_suggestion(self.user)
        
        assert len(ranked_suggestion) == 0