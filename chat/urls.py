from django.urls import path
from .views import perguntar, chat
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', chat, name='chat_home'), 
    path('perguntar/', perguntar, name='perguntar'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)