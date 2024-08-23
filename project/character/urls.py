from django.urls import path
from character.views import *

urlpatterns = [
    path('character/', CharacterDetailView.as_view(), name='character_detail'),
    path('create/', CharacterCreateView.as_view(), name="character_creation"),
]