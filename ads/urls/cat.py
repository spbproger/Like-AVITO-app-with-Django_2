from django.urls import path

from ads.views import category

urlpatterns = [
    path('', category.CategoryListView.as_view(), name='categories'),
    path('<int:pk>/', category.CategoryDetailView.as_view(), name='category'),
    path('update/<int:pk>/', category.CategoryUpdateView.as_view(), name='update_category'),
    path('create/', category.CategoryCreateView.as_view(), name='create_category'),
    path('delete/<int:pk>/', category.CategoryDeleteView.as_view(), name='delete_category'),
]
