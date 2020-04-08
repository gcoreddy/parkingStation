import time
import sys
from parking.models import TariffPlan, carDataDetails

class Ticket:
    def __init__(self, location) :
        self.outTime = time.time()
        car = self.__findVehical(location)
        self.carno  = car.carno
        self.inTime = float(car.inTime)
        self.location = car.location
        self.tariff    = car.tariff_plan
        self.ID        = self.__generateTicketID()
        self.amount   = None
        self.tariffMinutesDict = {"Hourly" : 3600, 
		                          "Daily" : 86400 }
		
    def __findVehical(self,location):
        return carDataDetails.objects.get(location=location)
				
    def __generateTicketID(self):
        import random
        ID = random.randint(1,100)
        return ID
		
    def __getTariffAmount(self):
        tariff = TariffPlan.objects.get(plan=self.tariff)
        return (tariff.cost,tariff.freetime)

    def __getTariffMinutes(self):  
        if self.tariff == "Hourly":
            minutes = 3600
        elif self.tariff == "Daily":
            minutes = 86400
        return minutes

    def __calAmount(self):
        cost,freetime = self.__getTariffAmount()
        if (self.outTime - self.inTime) < float(freetime)*60 :
            return 0
        else:
            tariffAmnt = self.tariffMinutesDict[self.tariff]
            totalTime  = self.outTime - self.inTime - float(freetime)*60
            price = (totalTime//int(tariffAmnt)+1) * int(cost)
            return price
			
    def createOrUpdateTariff(plan_name,plan_cost,plan_freetime):
        tarifPlansDict = {"TariffPlansInfo" : []}
        try:
            existingPlan = TariffPlan.objects.get(plan=plan_name)
            existingPlan.cost = plan_cost
            existingPlan.freetime=plan_freetime
            existingPlan.save()
        except TariffPlan.DoesNotExist:
            newPlan = TariffPlan(plan=plan_name,cost=plan_cost,freetime=plan_freetime)
            newPlan.save()

        for plan in TariffPlan.objects.all().values("plan","cost","freetime"):
            tarifPlansDict["TariffPlansInfo"].append(plan)
        print("tariffPlanDIctis:",tarifPlansDict)
        return tarifPlansDict

    def listTariffPlans():
        tarifPlansDict = {"TariffPlansInfo" : []}
        for plan in TariffPlan.objects.all().values("plan","cost","freetime"):
            tarifPlansDict["TariffPlansInfo"].append(plan)
        return tarifPlansDict
        
    def printTicket(self):
        self.amount = self.__calAmount()
        ticketDict = {"Car" : self.carno, "tariff" : self.tariff, 
		              "Location": self.location, "ID": self.ID, 
					  "Start" : time.strftime("%m/%d/%Y, %H:%M:%S",time.gmtime(float(self.inTime)))}
        ticketDict["Finish"] = time.strftime("%m/%d/%Y, %H:%M:%S",time.gmtime(float(self.outTime)))
        ticketDict["Fee"] = self.amount
        return ticketDict