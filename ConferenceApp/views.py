from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView, DetailView
# Create your views here.
def all_conferences(req):
    conferences=Conference.objects.all()
    return render(req,'Conference/liste.html',{"liste":conferences})
class ConferenceList(ListView):
    model=Conference
    context_object_name="liste"
    ordering=["start_date"]
    template_name="conference/liste.html"
class ConferenceDetail(DetailView):
    model=Conference
    context_object_name="conference"
    template_name="conference/details.html"
