from django.urls import path
from .views import (CreateFreelancerProfileView, CreateSkillView,
                     CreateProjectOfferView, UpdateFreelancerProfileView, UpdateProjectOfferView, 
                     DeleteSkillView, DeleteProjectOfferView, OwnProfileDetailView, OtherProfileDetailView)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('create/', CreateFreelancerProfileView.as_view(), name="profileCreate"),
    path('create/Project/', CreateProjectOfferView.as_view(), name="projectCreate"),
    path('create/Skill/', CreateSkillView.as_view(), name="skillCreate"),
    path('profileUpdate/<int:pk>/', UpdateFreelancerProfileView.as_view(), name="profileUpdate"),
    path('projectUpdate/<int:pk>', UpdateProjectOfferView.as_view(), name="projectUpdate"),
    path('skill/delete/<int:pk>/', DeleteSkillView.as_view(), name="skillDel"),
    path('project/delete/<int:pk>/', DeleteProjectOfferView.as_view(), name="projectDel"),
    path('profile/<int:pk>/', OwnProfileDetailView.as_view(), name="profile"),
    path('freelancer/<int:pk>/', OtherProfileDetailView.as_view(), name="freelancer"),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
