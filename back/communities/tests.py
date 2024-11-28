from django.test import TestCase
from accounts.models import User
from communities.models import Community

class UserCommunityAssignmentTest(TestCase):
    def setUp(self):
        """테스트 데이터 설정"""
        # 소득 분위별 커뮤니티 생성
        Community.objects.create(name='소득1분위', decile=1)
        Community.objects.create(name='소득2분위', decile=2)
        Community.objects.create(name='소득3분위', decile=3)

    def test_user_assigned_to_community(self):
        """사용자가 소득 분위에 따라 올바르게 커뮤니티에 할당되는지 테스트"""
        # 테스트 사용자 생성
        user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            income=3500,  # 소득 3500 -> 소득2분위에 해당
        )

        # 커뮤니티 할당 확인
        user.refresh_from_db()  # 데이터베이스에서 사용자 새로고침
        self.assertEqual(user.community.decile, 2)  # 소득2분위인지 확인

    def test_user_no_matching_community(self):
        """사용자가 소득 분위에 맞는 커뮤니티가 없을 경우"""
        user = User.objects.create(
            username='testuser2',
            email='testuser2@example.com',
            income=9999999,  # 너무 높은 소득 -> 매칭되지 않을 가능성
        )

        # 커뮤니티가 없으면 user.community는 None이어야 함
        user.refresh_from_db()
        self.assertIsNone(user.community)
