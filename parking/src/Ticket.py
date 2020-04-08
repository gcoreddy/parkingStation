import time
import sys
from parking.models import TariffPlan, carDataDetails

class Ticket:
    ''' Class used for update/create tariff plans and for
	    generating tickets with fare details for cars at exit.'''
		
    def __init__(self, location) :
        '''Constructor method'''
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
        ''' This method searches and returns in the database for car
		    based on location details provided'''
        return carDataDetails.objects.get(location=location)
				
    def __generateTicketID(self):
        ''' Method generates and returns an ID for each ticket.'''
        import random
        ID = random.randint(1,100)
        return ID
		
    def __getTariffAmount(self):
        ''' Method returns the cost and freetime for tariff plan selected.'''
        tariff = TariffPlan.objects.get(plan=self.tariff)
        return (tariff.cost,tariff.freetime)

    def __calAmount(self):
        ''' Method calculates the amount for the car at exit based on
		    intime,outtime and tariff plan selected at entry.'''

        # Get the cost and free time for the specific tariff plan.
        cost,freetime = self.__getTariffAmount()
        if (self.outTime - self.inTime) < float(freetime)*60 :
            # Return 0 if the outtime is less then the freetime of the plan.
            return 0
        else:

            # Calculate the total time of stay of a car minus free minutes multiplied by cost.
            tariffMnts = self.tariffMinutesDict[self.tariff]
            totalTime  = self.outTime - self.inTime - float(freetime)*60
            price = (totalTime//int(tariffMnts)+1) * int(cost)
            return price
			
    def createOrUpdateTariff(plan_name,plan_cost,plan_freetime):
        ''' Creates or updates the tariff plan details.'''
        tarifPlansDict = {"TariffPlansInfo" : []}
        try:
            # Check whether tariff plan already exist and update the plan if found.
            existingPlan = TariffPlan.objects.get(plan=plan_name)
            existingPlan.cost = plan_cost
            existingPlan.freetime=plan_freetime
            existingPlan.save()
        except TariffPlan.DoesNotExist:

            # Create a plan with the details passed.
            newPlan = TariffPlan(plan=plan_name,cost=plan_cost,freetime=plan_freetime)
            newPlan.save()

        # Display all the existing tariff plan details.
        for plan in TariffPlan.objects.all().values("plan","cost","freetime"):
            tarifPlansDict["TariffPlansInfo"].append(plan)
        return tarifPlansDict
		
    def printTicket(self):
	    ''' Generates a ticket to the car owner with cost details at exit.'''

        # Calling calulate method to get the cost for the user.
        self.amount = self.__calAmount()
        ticketDict = {"Car" : self.carno, "tariff" : self.tariff, 
		              "Location": self.location, "ID": self.ID, 
					  "Start" : time.strftime("%m/%d/%Y, %H:%M:%S",time.gmtime(float(self.inTime)))}
        ticketDict["Finish"] = time.strftime("%m/%d/%Y, %H:%M:%S",time.gmtime(float(self.outTime)))
        ticketDict["Fee"] = self.amount
        return ticketDict