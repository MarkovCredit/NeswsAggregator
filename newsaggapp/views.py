import pytz

from django.views.generic import ListView
from django.shortcuts import redirect, render

from .models import Article

class HomePageView(ListView):
    template_name = "homepage.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.filter().order_by("-pub_date")[:10]
        return context

    # def set_timezone(request):
    #     if request.method == 'POST':
    #         request.session['django_timezone'] = request.POST['timezone']
    #         return redirect('/')
    #     else:
    #         return render(request, 'template.html', {'timezones': pytz.common_timezones})

        