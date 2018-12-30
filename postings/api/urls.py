from django.conf.urls import url
from .views import BlogPostRudView, BlogPostCreateListSearchView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', BlogPostRudView.as_view(), name='post-rud'),
    url(r'^create-post/$', BlogPostCreateListSearchView.as_view(), name='create-list-search'),
]
