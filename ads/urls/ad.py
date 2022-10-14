from django.urls import path

from ads.views import ad

urlpatterns = [
    path('', ad.AdListView.as_view(), name='ads'),
    path('<int:pk>/', ad.AdDetailView.as_view(), name='ad'),
    path('create/', ad.AdCreateView.as_view(), name='create_ad'),
    path('update/<int:pk>/', ad.AdUpdateView.as_view(), name='update_ad'),
    path('delete/<int:pk>/', ad.AdDeleteView.as_view(), name='delete_ad'),
    path('upload_image/<int:pk>/', ad.AdImageView.as_view(), name='upload_image'),
]
