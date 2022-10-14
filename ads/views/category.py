from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, ListView, DeleteView, CreateView
from ads.models import Category
import json
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        categories = self.object_list.order_by('name')

        response = []
        for cat in categories:
            response.append({
                "id": cat.id,
                "name": cat.name
            })
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)
        category = Category.objects.create(name=cat_data['name'])
        return JsonResponse({'id': category.id, 'name': category.name}, safe=False,
                            json_dumps_params={"ensure_ascii": False})


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        cat = self.get_object()

        return JsonResponse({
                "id": cat.id,
                "name": cat.name
            }, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        category_data = json.loads(request.body)
        category = self.object

        category.name = category_data.get('name')

        category.save()

        response = {
            'id': category.id,
            'name': category.name
        }

        return JsonResponse(response, json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'OK'})
