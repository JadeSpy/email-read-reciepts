from django.urls import path, include
from django.http import HttpResponse
from . import views

app_name = 'tracking'
urlpatterns = [
    path("create-tracker/", views.create_tracker_form, name='create_tracker'),
    path("tracker-image-download/<uuid:id>/", views.get_identifier_image, name="url_of_emailed_tracker_image"),
    path("",lambda request: HttpResponse("Hello, Stranger.")),
    path("tracker-created-successfully/<uuid:pk>", views.trackerCreatedSuccessfully.as_view(), name="tracker_created_successfully"),

    #path('', views.IndexView.as_view(), name='index'),
    #path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #path('<int:question_id>/vote/', views.vote, name='vote'),
]