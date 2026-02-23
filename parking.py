'''
parking lot class: 10 small spots, 15 medium spots, 5 large spots
definition for adding a car to the lot, and updating lot size (assuming we wont admit vehicles if we dont
have space for them). When we add a vehicle we also need to keep a tab of when they entered, so we can apply the fee
when they exit. Another definition for exiting a vehicle
vehicle types mapping: motorcycle: (1, small), car: (3, medium), truck:(5, large)
'''
'''
New requirement: 3 Floors
Floor class which is an array of dictionaries.
'''
from datetime import datetime
import math
from abc import ABC, abstractmethod

VEHICLE_TYPE = {"motorcycle": (1, "small"), "car": (3, "medium"), "truck": (5, "large")}

class FeeStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, time_spent, base_rate):
        pass

class FlatRate(FeeStrategy):
    def calculate_fee(self, time_spent, base_rate):
        hours = math.ceil(time_spent.total_seconds() / 3600)
        return hours * base_rate

class WeekendSurge(FeeStrategy):
    def calculate_fee(self, time_spent, base_rate):
        hours = math.ceil(time_spent.total_seconds() / 3600)
        if datetime.now().weekday() in [5, 6]:
            return hours * base_rate * 2
        return hours * base_rate
    
        
class Floor:
    def __init__(self):
        self.spots = {"small": 10, "medium": 15, "large": 5}
    
    def has_spot(self, spot_type) -> bool:
        if self.spots[spot_type]:
            return True
        else:
            return False
    
    def park(self, spot_type) -> bool:
        if self.spots[spot_type]:
            self.spots[spot_type] -= 1
            return True
        else:
            return False
    
    def free(self, spot_type) -> None:
        self.spots[spot_type] += 1


class ParkingLot:
    def __init__(self, numFloors, fee_strategy):
        self.floors = [Floor() for _ in range(numFloors)]
        self.vehicles = {} # vehicle_id: (type, enter time, floor_number)
        self.fee_strategy = fee_strategy

    def addCar(self, vehicle_id, vehicle_type) -> bool:
        spot_type = VEHICLE_TYPE[vehicle_type][1]
        for i, floor in enumerate(self.floors):
            if floor.has_spot(spot_type):
                floor.park(spot_type)
                self.vehicles[vehicle_id] = (vehicle_type, datetime.now(), i)
                return True
        return False
            
    # -1 for graceful error handling if vehicle not found
    def removeCar(self, vehicle_id) -> float:
        if vehicle_id in self.vehicles:
            vehicle_type, enter_time, floor_number = self.vehicles[vehicle_id]
        else:
            return -1.0

        # clear up spot and vehicle dictionary
        spot_type = VEHICLE_TYPE[vehicle_type][1]
        floor = self.floors[floor_number]
        floor.free(spot_type)

        self.vehicles.pop(vehicle_id)

        # calculate fees
        fee = VEHICLE_TYPE[vehicle_type][0]
        time_spent = datetime.now() - enter_time
        return self.fee_strategy.calculate_fee(time_spent, fee)
        

    
