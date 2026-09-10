from django.urls import path

from apps.transaction.api.views import (
    CheckCodeView,
    RequiredImagesView,
    ShopLookupView,
    BonusSummaryView,
    BonusHistoryView,
    LeaderboardView,
    ChallengeListView,
    AnalyticsView
)

urlpatterns = [
    path('bonus/lookup-code/', CheckCodeView.as_view(), name='bonus-lookup-code'),
    path('bonus/lookup-shop/', ShopLookupView.as_view(), name='bonus-lookup-shop'),
    path('bonus/required-images/', RequiredImagesView.as_view(), name='bonus-required-images'),
    path('bonus/summary/', BonusSummaryView.as_view(), name='bonus-summary'),
    path('bonus/history/', BonusHistoryView.as_view(), name='bonus-history'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('challenges/', ChallengeListView.as_view(), name='challenges'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]
