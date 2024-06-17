from django.urls import path
from .views import MattressScrapperView

urlpatterns = [
    path('scrape/', MattressScrapperView.as_view()),
]