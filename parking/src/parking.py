import time
import sys
import json
import django
from parking.models import TariffPlan, carDataDetails, ParkingLevel 
from parking.src.Ticket import Ticket
from parking.src.parkingExceptions import parkingExceptionsDict, LevelWithTheSameName, ParkingLevelDoesntExist, NoSpaceLeftInParking, CarWithSameNumExist

class ParkingStation:
    def __init__(self):
        self.jsonDec = json.decoder.JSONDecoder()
	
    def __displayLevels(self):
        levelInfoDict = {"LevelInfo" : []}
        for level in ParkingLevel.objects.all().values("level_num","free_spots","occupied_spots","total_spots"):
            levelInfoDict["LevelInfo"].append(level)
        return levelInfoDict
		
    def deleteLevel(self,level_name):
        ParkingLevel.objects.filter(level_num=level_name).delete()
        
    def addLevel(self,level_name,total_spots):
        if len(ParkingLevel.objects.filter(level_num=level_name)) > 0:
            print("I am gereeeeeeeeeeeeeeeeeeeeeee",parkingExceptionsDict["LevelWithTheSameName"])
            return parkingExceptionsDict["LevelWithTheSameName"]
        free_spots  = list(range(1,int(total_spots)+1))
        occupied_spots = []
        level = ParkingLevel(level_num=level_name,total_spots=total_spots,free_spots=json.dumps(list(free_spots)),occupied_spots=json.dumps(list(occupied_spots)))
        level.save()
        return self.__displayLevels()

    def __getAvailableLocation(self):
        location = None
        if len(ParkingLevel.objects.all()) == 0:
            raise ParkingLevelDoesntExist
        for level in ParkingLevel.objects.all():
            free_spots = list(self.jsonDec.decode(level.free_spots))
            if len(free_spots) > 0:
                assignedSpot = free_spots[-1]
                location = level.level_num + "_" + str(assignedSpot)
                break
        if location is None: raise NoSpaceLeftInParking
        return location
        
    def __checkCarNo(self,car_num):
        try:
            car = carDataDetails.objects.get(carno=car_num)
        except carDataDetails.DoesNotExist:
            print("I am here in exception")
            pass
        else:
            raise CarWithSameNumExist

    def addCar(self, car_num, plan_name):
        try:
            tariff = TariffPlan.objects.get(plan=plan_name)
            inTime=time.time()
            location = self.__getAvailableLocation()
            self.__checkCarNo(car_num)
            newCar = carDataDetails.objects.create(carno=car_num,tariff_plan=plan_name,inTime=inTime,location=location)
            newCar.save()
            self.__assignSpot(location)
            receipt = {"car" : car_num,"tariff" : plan_name, "location" : location, "start" : time.strftime("%m/%d/%Y, %H:%M:%S",time.gmtime(float(inTime)))}
        except ParkingLevelDoesntExist:
            receipt = parkingExceptionsDict["ParkingLevelDoesntExist"]
        except NoSpaceLeftInParking:
            receipt = parkingExceptionsDict["NoSpaceLeftInParking"]
        except CarWithSameNumExist:
            receipt = parkingExceptionsDict["CarWithSameNumExist"]
        except TariffPlan.DoesNotExist:
            receipt = parkingExceptionsDict["TariffPlanDoesntExist"]
        finally:
            return receipt
            
    def removeCar(self, location):
        ''' This method removes a car based on specific location 
		    from the parking space and make it available for next cars. 
		'''
        try:
            ticket = Ticket(location)
            receipt = ticket.printTicket()
            carDataDetails.objects.get(location=location).delete()
            self.__unAssignSpot(location)
        except TariffPlan.DoesNotExist:
            receipt = parkingExceptionsDict["TariffPlanDoesntExist"]
        except carDataDetails.DoesNotExist:
            receipt = parkingExceptionsDict["LocationEmpty"]
        except carDataDetails.MultipleObjectsReturned:
            receipt = parkingExceptionsDict["MultipleCarsWithSameLocation"]
        finally:
            return receipt
		
    def displayCars(self):
        ''' This method diplays all the cars that are parked. '''
        carDetailsDict = {"cars": []}
        for car in carDataDetails.objects.values("carno", "tariff_plan", "location", "inTime"):
            car["inTime"] = time.strftime("%m/%d/%Y, %H:%M:%S",time.gmtime(float(car["inTime"])))
            carDetailsDict["cars"].append(car)
        return carDetailsDict
		
    def __assignSpot(self,location):
        '''This method assigns an available spot to the car 
		   in the specified level.
		'''
        level = ParkingLevel.objects.get(level_num=location.split("_")[0])
        free_spots = list(self.jsonDec.decode(level.free_spots))
        assignedSpot = location.split("_")[1]
        free_spots.remove(int(assignedSpot))
        level.free_spots = json.dumps(list(free_spots))
        occupiedSlots = list(self.jsonDec.decode(level.occupied_spots))
        occupiedSlots.append(assignedSpot)
        level.occupied_spots = json.dumps(list(occupiedSlots))
        level.save()
        return location

    def __unAssignSpot(self,location):
        '''This method un assigns occpied spot of the car at exit.'''
        level = ParkingLevel.objects.get(level_num=location.split("_")[0])
        assignedSpot = location.split("_")[1]
        free_spots = list(self.jsonDec.decode(level.free_spots))
        free_spots.append(int(assignedSpot))
        level.free_spots = json.dumps(list(free_spots))
        occupiedSlots = list(self.jsonDec.decode(level.occupied_spots))
        occupiedSlots.remove(assignedSpot)
        level.occupied_spots = json.dumps(list(occupiedSlots))
        level.save()
