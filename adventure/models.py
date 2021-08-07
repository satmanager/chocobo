from django.db import models
import re #Import for vehicle number_plate validation

# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self) -> list:
        if self.passengers == 2:
            distribution = [[True,True],[False,False]]
        elif self.passengers == 3:
            distribution = [[True,True],[True,False]]
        elif self.passengers == 4:
            distribution = [[True,True],[True,True]]
        else: 
            distribution = [[True,False],[False,False]]
        return distribution
    


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"
    
    def is_finished(self):
        return not self.end is None  

#Number Plate Validation
def validate_number_plate(plate) -> bool:
    r = re.compile('[A-Z]{2}-[0-9]{2}-[0-9]{2}')
    return r.match(plate)