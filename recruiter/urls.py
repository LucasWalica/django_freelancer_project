from django.urls import path
from .views import CreateRecruiterProfile, CreateRecruiterProject, UpdateRecruiterProfile, DeleteRecruiterProject, OwnRecruiterView

urlpatterns = [
    path('<int:pk>/', OwnRecruiterView.as_view(), name="recruiter"),
    path('createRecruiter/', CreateRecruiterProfile.as_view(), name="createRecruiter"),    
    path('recruiter/projectCreate/', CreateRecruiterProject.as_view(), name="freeProjectCreate"),
    path('recruiter/<int:pk>/update/', UpdateRecruiterProfile.as_view(), name="updateRecruiter"),
    path('recruiter/<int:pk>/delete/', DeleteRecruiterProject.as_view(), name="deleteRecruiter"),
]
