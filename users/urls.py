from django.urls import path

from users import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='users'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user'),
    path('create/', views.UserCreateView.as_view(), name='create_user'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='update_user'),
    path('delete/<int:pk>/', views.UserDeleteView.as_view(), name='delete_user'),
]
