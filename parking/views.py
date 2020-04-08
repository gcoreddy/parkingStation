from django.shortcuts import render
from django.shortcuts import HttpResponse
from parking.models import TariffPlan, carDataDetails
from parking.src.Ticket import Ticket
from parking.src.parking import ParkingStation
from parking.src import parkingExceptions
from django.http import JsonResponse
        
def getQuery(request):
    pstation = ParkingStation()
    if request.method == 'GET':
        return render(request, 'index.html', {})
    elif request.method == 'POST':
        if request.POST['OPTION'] == "1":
            output = Ticket.createOrUpdateTariff(request.POST['plan'],request.POST['cost'],request.POST['freetime'])
            return JsonResponse(output,safe=False)
        elif request.POST['OPTION'] == "2":
            return JsonResponse(pstation.addCar(request.POST['car_num'],request.POST['tariff_plan']),safe=False)
        elif request.POST['OPTION'] == "3":
            return JsonResponse(pstation.removeCar(request.POST['location']),safe=False)
        elif request.POST['OPTION'] == "4":
            return JsonResponse(pstation.displayCars(),safe=False)
        elif request.POST['OPTION'] == "5":
            return JsonResponse(pstation.addLevel(request.POST['level_name'],request.POST['parking_spots']),safe=False)
    else:
        print(request.POST['OPTION'])
