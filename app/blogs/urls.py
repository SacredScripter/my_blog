from django.urls import path
from blogs import views as blogs_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #path('', tutorials_views.index, name='home'),
    path('', blogs_views.index.as_view(), name='home'),
    path('api/blogs/', blogs_views.blog_list),
    path('api/blogs/<int:pk>/', blogs_views.blog_detail),
    path('api/blogs/published/', blogs_views.blog_list_published)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)