from django.urls import path, include
from rest_framework.routers import DefaultRouter
from projects.views import (
    ProjectViewSet, PropertyViewSet,
    ProjectListView,ProjectByTypeView,
    ProjectSearchByNameView, ProjectByLocationView,
    FeaturedPropertyListView, LatestBlogPostCreateView,
    ClientReviewCreateView, ClientReviewListView
    )


# রাউটার সেটআপ
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'properties', PropertyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get_all_Projects/', ProjectListView.as_view(), name='project-list-all'),
    path('get_type_base_projects/', ProjectByTypeView.as_view(), name='project-by-type'),
    path('get_name_base_projects/', ProjectSearchByNameView.as_view(), name='project-search-by-name'),
    path('get_projects_by_locations/<str:location>/', ProjectByLocationView.as_view(), name='project-by-location'),
    path('get_all_featured_properties/',FeaturedPropertyListView.as_view(),name='featured-properties'),
    path('latest_blog_posts/', LatestBlogPostCreateView.as_view(), name='latest-blog-posts'),
    path('create_client_reviews/', ClientReviewCreateView.as_view(), name='client-review-create'),
    path('get_client_reviews/', ClientReviewListView.as_view(), name='client-review-list'),

]