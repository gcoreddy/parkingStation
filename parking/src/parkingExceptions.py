class NoSpaceLeftInParking(Exception):
    '''Exception for no space left in the parking.'''
    pass

class CarWithSameNumExist(Exception):
    '''Exception if car is already parked with the same number.'''
    pass

class LocationEmpty(Exception):
    '''Exception if user tries to remove a parking slot which is not occupied.'''
    pass

class NoCarFound(Exception):
    '''Exception if there is no car with the name specified.'''
    pass
	
class InvalidTariff(Exception):
    '''Exception if user selects invalid tariff plan.'''
    pass
	
class NoCarstoDisplay(Exception):
    '''Exception if there are no cars exists in the parking.'''
    pass
	
class LevelWithTheSameName(Exception):
    '''Exception while creating a new level.
	   throws an exception if there is a level with the same name exist'''
    pass
	
class TariffPlanDoesntExist(Exception):
    '''Exception if there is no tariffPlan defined.'''
    pass
	
class MultipleCarsWithSameLocation(Exception):
    '''Exception if database shows multiple cars with the same location spot'''
    pass
	
class ParkingLevelDoesntExist(Exception):
    '''Exception if there is no Parking level exist in the station.'''
    pass
	
parkingExceptionsDict = {
             "NoSpaceLeftInParking"  : { "Status" : "Fail", 
			                              "Reason" : "No Space left in the parking."
							           },
			  "CarWithSameNumExist" : { "Status" : "Fail",
			                             "Reason" : "Car with same number already exist in the parking."
									   },
			  "LocationEmpty"       :  { "Status" : "Fail",
                                         "Reason" : "Specified parking location is already empty."			  
									   },
			  "NoCarFound"          :  { "Status" : "Fail",
			                             "Reason" : "No cars found in the parking. Parking is empty."
										},
			  "InvalidTariff"        :  { "Status" : "Fail",
			                              "Reason" : "Traiff Plan selected is invalid."
										},
			   "NoCarstoDisplay"     :  { "Status" : "Success",
			                              "Message" : "Parking station doesn't have parked cars."
			                           },
			    "LevelWithTheSameName" : { "Status" : "Fail", 
				                           "Reason" : "Level with the same name already exist."
										},
				"TariffPlanDoesntExist" : {"Status" : "Fail",
				                           "Error"  : "Tariff Plan is not yet defined in the database."
				                        },
	  "MultipleCarsWithSameLocation" : { "Status" : "Fail",
				                         "Error" : "Multiple cars are assigned with same location Number."
			                            },
			"ParkingLevelDoesntExist" : { "Status" : "Fail",
			                             "Error"  : "Parking Level doesn't exist or not yet added."
	                                    },
			"UnExpectedError"         : {"Status" : "Fail",
			                             "Error"  :  "Unexpected error occured"
										 },
	}