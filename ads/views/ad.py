from django.http import JsonResponse

from django.utils.decorators import method_decorator

from django.views.generic import DetailView, UpdateView, ListView, DeleteView, CreateView

from Homework_28v2 import settings
from ads.models import Ad, Category
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from users.models import User


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        ads = self.object_list.order_by('-price')

        paginator = Paginator(ads, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        response_ads = []
        for ad in page_obj:
            response_ads.append({
                    'id': ad.id,
                    'author_id': ad.author_id,
                    'author': str(ad.author),
                    'name': ad.name,
                    'price': ad.price,
                    'description': ad.description,
                    'is_published': ad.is_published,
                    'image': ad.image.url if ad.image else None,
                    'category_id': ad.category_id,
                    'category': str(ad.category)
                })

        response = {
            "items": response_ads,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            'id': ad.id,
            'author_id': ad.author_id,
            'author': str(ad.author),
            'name': ad.name,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,
            'image': ad.image.url if ad.image else None,
            'category_id': ad.category_id,
            'category': str(ad.category)
                }, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category']

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        new_ad = Ad.objects.create(
            name=ad_data['name'],
            author=get_object_or_404(User, pk=ad_data['author']),
            price=ad_data['price'],
            description=ad_data['description'],
            is_published=ad_data['is_published'],
            category=get_object_or_404(Category, pk=ad_data['category']))

        return JsonResponse({
            'id': new_ad.id,
            'name': new_ad.name,
            'author': new_ad.author.username,
            'price': new_ad.price,
            'description': new_ad.description,
            'is_published': new_ad.is_published,
            'category': new_ad.category.name,
            'image': new_ad.image.url if new_ad.image else None
        }, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'author', 'price', 'description', 'category']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        self.object.name = ad_data["name"]

        self.object.author_id = ad_data["author_id"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data["description"]
        self.object.category_id = ad_data["category_id"]
        self.object.save()

        response = {
            'id': self.object.id,
            'author_id': self.object.author_id,
            'name': self.object.name,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'image': self.object.image.url if self.object.image else None,
            'category_id': self.object.category_id,
        }

        return JsonResponse(response,
                            json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ['name', 'image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image", None)
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published,
            'category_id': self.object.category_id,
            'image': self.object.image.url if self.object.image else None,
            }, json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'OK'})
