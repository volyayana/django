from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from csv import DictReader
from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    with open(BUS_STATION_CSV, encoding='utf8') as csvfile:
        stations = list(DictReader(csvfile))
    paginator = Paginator(stations, 10)
    current_page = int(request.GET.get("page", 1))
    page = paginator.get_page(current_page)
    context = {
         'bus_stations': page.object_list,
         'page': page,
    }
    return render(request, 'stations/index.html', context)
