
from django.views import View
from django.http import HttpResponse

class HomeView(View):

    def get(self, request):
        return HttpResponse(f'This is home')

class PostView(View):

    def get(self, request):
        return HttpResponse(f'This is a blog post')