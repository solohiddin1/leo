from django.core.cache import cache

from apps.shared.utils.utils import success_response
from apps.transaction.repositories.leaderboard_repo import LeaderboardRepo
from apps.user.models import User


class LeaderboardService:
    TOP_N = 10
    CACHE_KEY = "leaderboard_top_10"
    CACHE_TIMEOUT = 300  # 5 minutes

    @staticmethod
    def get_leaderboard(user: User):
        from apps.transaction.services.bonus_service import BonusService

        top_leaderboard = cache.get(LeaderboardService.CACHE_KEY)

        if top_leaderboard is None:
            ranked_users = LeaderboardRepo.get_ranked_users(LeaderboardService.TOP_N)
            top_leaderboard = [
                {
                    'id': u.id,
                    'username': u.username,
                    'first_name': u.first_name,
                    'last_name': u.last_name,
                    'total_earned': u.calc_total_earned,
                    'rank': u.rank,
                }
                for u in ranked_users
            ]
            cache.set(LeaderboardService.CACHE_KEY, top_leaderboard, LeaderboardService.CACHE_TIMEOUT)

        leaderboard_data = [
            {**entry, 'is_me': entry['id'] == user.id}
            for entry in top_leaderboard
        ]

        my_entry = next((item for item in leaderboard_data if item['is_me']), None)
        if my_entry:
            my_rank = my_entry['rank']
        else:
            my_user_total = BonusService.get_user_total_earned(user)
            better_users_count = LeaderboardRepo.count_users_ahead_of(my_user_total)
            my_rank = better_users_count + 1

            leaderboard_data.append({
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'total_earned': my_user_total,
                'rank': my_rank,
                'is_me': True,
            })

        return success_response({
            'leaderboard': leaderboard_data,
            'my_rank': my_rank
        })
