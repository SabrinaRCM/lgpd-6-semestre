from peewee import *
from geopy.distance import geodesic

database = SqliteDatabase("clients.db")

class Distance:
    distance = 9999

class BaseModel(Model):
    class Meta:
        database = database

class Local(BaseModel):
    id = BigIntegerField(primary_key=True)
    nome = CharField(null=True)
    tipo = CharField(null=True)
    lat = CharField(null=True)
    long = CharField(null=True)

    class Meta:
        database = database

    def Distance(lat, long, dist):
        listOfPoints = []
        userLocation = (lat, long)

        rows = Local.select()
        listLocals = list(rows)
        for local in listLocals:
            localLocation = (local.lat, local.long)
            distance = geodesic(userLocation, localLocation).m
            if (dist >= distance):
                listOfPoints.append(local.nome + "|" + local.tipo + "|" + str(round(distance)))
        return listOfPoints
    
    def VerifyMoreProximity(listOfPoints):
        for point in listOfPoints:
            splittedPoint = point.split("|")
            distance = splittedPoint[2]
            if float(distance) < float(Distance.distance):
                Distance.distance = distance
                moreProximity = point

        return moreProximity