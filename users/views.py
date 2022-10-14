from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, ListView, DeleteView, CreateView
from Homework_28v2 import settings
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from users.models import User, Location


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.annotate(ads_published=Count('ad', filter=Q(ad__is_published__gte=True)))
        self.object_list = self.object_list.order_by('username')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        response_user = []
        for user in page_obj:
            response_user.append({
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                    'age': user.age,
                    'locations': list(map(str, user.locations.all())),
                    'ads_published': user.ads_published
                })

        response = {
            "items": response_user,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'locations': list(map(str, user.locations.all()))
            }, safe=False, json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'role', 'password', 'age', 'locations']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        user = User.objects.create(
            username=user_data.get('username'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            role=user_data.get('role'),
            password=user_data.get('password'),
            age=user_data.get('age')
        )

        location, created = Location.objects.get_or_create(name=str(user_data.get('locations')))
        user.locations.add(location)

        response = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'age': user.age,
                'locations': list(map(str, user.locations.all()))
        }

        return JsonResponse(response,
                            json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'role', 'password', 'age', 'locations']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)
        user = self.object

        user.username = user_data.get('username')
        user.password = user_data.get('password')
        user.first_name = user_data.get('first_name')
        user.last_name = user_data.get('last_name')
        user.age = user_data.get('age')
        user.location, created = Location.objects.get_or_create(name=user_data.get('locations'))

        user.save()

        response = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'locations': list(map(str, user.locations.all()))
        }

        return JsonResponse(response,
                            json_dumps_params={"ensure_ascii": False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'OK'})
