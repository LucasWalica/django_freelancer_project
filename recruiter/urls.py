from django.urls import path
from .views import (CreateRecruiterProfile, CreateRecruiterProject,
                    UpdateRecruiterProfile, DeleteRecruiterProject,
                    OwnRecruiterView, UpdateRecruiterProject, 
                    FreelancerProjectListAndFreelancers, RecruiterProjectDetailView, 
                    OtherProfileDetailView)

urlpatterns = [
    path('me/<int:pk>/', OwnRecruiterView.as_view(), name="recruiter"),
    path('createRecruiter/', CreateRecruiterProfile.as_view(), name="createRecruiter"),    
    path('recruiter/projectCreate/', CreateRecruiterProject.as_view(), name="freeProjectCreate"),
    path('recruiter/<int:pk>/update/', UpdateRecruiterProfile.as_view(), name="updateRecruiter"),
    path('deleteProject/<int:pk>/', DeleteRecruiterProject.as_view(), name="deleteRecruiterProject"),
    path('updateProject/<int:pk>/', UpdateRecruiterProject.as_view(), name="updateRecruiterProject"),
    path('search/', FreelancerProjectListAndFreelancers.as_view(), name="recruiterSearch"),
    path('project/<int:pk>/', RecruiterProjectDetailView.as_view(), name="recruiterProject"),
    path('<int:pk>/',OtherProfileDetailView.as_view(), name="otherRecruiter" )
]
