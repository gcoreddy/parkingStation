class NoSpaceLeft(Exception):
    pass
   
class vehicalAlreadyAdded(Exception):
    pass
   
class vehicalAlreadyRemoved(Exception):
    pass
	
class NoSpaceLeftInParking(Exception):
    pass

class CarWithSameNumExist(Exception):
    pass

class LocationEmpty(Exception):
    pass

class NoCarFound(Exception):
    pass
	
class InvalidTariff(Exception):
    pass
	
class NoCarstoDisplay(Exception):
    pass
	
class LevelWithTheSameName(Exception):
    pass
	
class TariffPlanDoesntExist(Exception):
    pass
	
class MultipleCarsWithSameLocation(Exception):
    pass
	
class ParkingLevelDoesntExist(Exception):
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