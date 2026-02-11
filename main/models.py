from django.db import models
from django.contrib.auth.models import User
from django.apps import apps

# Create your models here.
User = User

class Subject(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.title.capitalize()}'
    


kenya_constituencies = {
    "Mombasa": [
        "Changamwe", "Jomvu", "Kisauni", "Nyali", "Likoni", "Mvita"
    ],

    "Kwale": [
        "Msambweni", "Lunga Lunga", "Matuga", "Kinango"
    ],

    "Kilifi": [
        "Kilifi North", "Kilifi South", "Kaloleni",
        "Rabai", "Ganze", "Malindi", "Magarini"
    ],

    "Tana River": [
        "Garsen", "Galole", "Bura"
    ],

    "Lamu": [
        "Lamu East", "Lamu West"
    ],

    "Taita Taveta": [
        "Taveta", "Wundanyi", "Mwatate", "Voi"
    ],

    "Garissa": [
        "Garissa Township", "Balambala", "Lagdera",
        "Dadaab", "Fafi", "Ijara"
    ],

    "Wajir": [
        "Wajir North", "Wajir East", "Tarbaj",
        "Wajir West", "Eldas", "Wajir South"
    ],

    "Mandera": [
        "Mandera West", "Banissa", "Mandera North",
        "Mandera South", "Mandera East", "Lafey"
    ],

    "Marsabit": [
        "Moyale", "North Horr", "Saku", "Laisamis"
    ],

    "Isiolo": [
        "Isiolo North", "Isiolo South"
    ],

    "Meru": [
        "Igembe South", "Igembe Central", "Igembe North",
        "Tigania West", "Tigania East", "North Imenti",
        "Buuri", "Central Imenti", "South Imenti"
    ],

    "Tharaka Nithi": [
        "Maara", "Chuka/Igambang'ombe", "Tharaka"
    ],

    "Embu": [
        "Manyatta", "Runyenjes", "Mbeere South", "Mbeere North"
    ],

    "Kitui": [
        "Mwingi North", "Mwingi West", "Mwingi Central",
        "Kitui West", "Kitui Rural", "Kitui Central",
        "Kitui East", "Kitui South"
    ],

    "Machakos": [
        "Masinga", "Yatta", "Kangundo",
        "Matungulu", "Kathiani", "Mavoko",
        "Machakos Town", "Mwala"
    ],

    "Makueni": [
        "Mbooni", "Kilome", "Kaiti",
        "Makueni", "Kibwezi West", "Kibwezi East"
    ],

    "Nyandarua": [
        "Kinangop", "Kipipiri", "Ol Kalou",
        "Ol Jorok", "Ndaragwa"
    ],

    "Nyeri": [
        "Tetu", "Kieni", "Mathira",
        "Othaya", "Mukurweini", "Nyeri Town"
    ],

    "Kirinyaga": [
        "Mwea", "Gichugu", "Ndia", "Kirinyaga Central"
    ],

    "Murang'a": [
        "Kangema", "Mathioya", "Kiharu",
        "Kigumo", "Maragwa", "Kandara", "Gatanga"
    ],

    "Kiambu": [
        "Gatundu South", "Gatundu North", "Juja",
        "Thika Town", "Ruiru", "Githunguri",
        "Kiambu", "Kiambaa", "Kabete",
        "Kikuyu", "Limuru", "Lari"
    ],

    "Turkana": [
        "Turkana North", "Turkana West", "Turkana Central",
        "Loima", "Turkana South", "Turkana East"
    ],

    "West Pokot": [
        "Kapenguria", "Sigor", "Kacheliba", "Pokot South"
    ],

    "Samburu": [
        "Samburu West", "Samburu North", "Samburu East"
    ],

    "Trans Nzoia": [
        "Kwanza", "Endebess", "Saboti", "Kiminini", "Cherangany"
    ],

    "Uasin Gishu": [
        "Soy", "Turbo", "Moiben",
        "Ainabkoi", "Kapseret", "Kesses"
    ],

    "Elgeyo Marakwet": [
        "Marakwet East", "Marakwet West",
        "Keiyo North", "Keiyo South"
    ],

    "Nandi": [
        "Tinderet", "Aldai", "Nandi Hills",
        "Chesumei", "Emgwen", "Mosop"
    ],

    "Baringo": [
        "Tiaty", "Baringo North", "Baringo Central",
        "Baringo South", "Mogotio", "Eldama Ravine"
    ],

    "Laikipia": [
        "Laikipia West", "Laikipia East", "Laikipia North"
    ],

    "Nakuru": [
        "Molo", "Njoro", "Naivasha", "Gilgil",
        "Kuresoi South", "Kuresoi North",
        "Subukia", "Rongai", "Bahati",
        "Nakuru Town West", "Nakuru Town East"
    ],

    "Narok": [
        "Kilgoris", "Emurua Dikirr", "Narok North",
        "Narok East", "Narok South", "Narok West"
    ],

    "Kajiado": [
        "Kajiado North", "Kajiado Central",
        "Kajiado East", "Kajiado West", "Kajiado South"
    ],

    "Kericho": [
        "Kipkelion East", "Kipkelion West",
        "Ainamoi", "Bureti", "Belgut", "Sigowet/Soin"
    ],

    "Bomet": [
        "Sotik", "Chepalungu", "Bomet East",
        "Bomet Central", "Konoin"
    ],

    "Kakamega": [
        "Lugari", "Likuyani", "Malava", "Lurambi",
        "Navakholo", "Mumias West", "Mumias East",
        "Matungu", "Butere", "Khwisero",
        "Shinyalu", "Ikolomani"
    ],

    "Vihiga": [
        "Vihiga", "Sabatia", "Hamisi", "Luanda", "Emuhaya"
    ],

    "Bungoma": [
        "Mount Elgon", "Sirisia", "Kabuchai", "Bumula",
        "Kanduyi", "Webuye East", "Webuye West",
        "Kimilili", "Tongaren"
    ],

    "Busia": [
        "Teso North", "Teso South", "Nambale",
        "Matayos", "Butula", "Funyula", "Budalangi"
    ],

    "Siaya": [
        "Ugenya", "Ugunja", "Alego Usonga",
        "Gem", "Bondo", "Rarieda"
    ],

    "Kisumu": [
        "Kisumu East", "Kisumu West", "Kisumu Central",
        "Seme", "Nyando", "Muhoroni", "Nyakach"
    ],

    "Homa Bay": [
        "Kasipul", "Kabondo Kasipul", "Karachuonyo",
        "Rangwe", "Homa Bay Town", "Ndhiwa",
        "Mbita", "Suba"
    ],

    "Migori": [
        "Rongo", "Awendo", "Suna East", "Suna West",
        "Uriri", "Nyatike", "Kuria West", "Kuria East"
    ],

    "Kisii": [
        "Bonchari", "South Mugirango", "Bomachoge Borabu",
        "Bomachoge Chache", "Nyaribari Masaba",
        "Nyaribari Chache", "Kitutu Chache North",
        "Kitutu Chache South", "Bobasi"
    ],

    "Nyamira": [
        "West Mugirango", "North Mugirango",
        "Borabu", "Kitutu Masaba"
    ],

    "Nairobi": [
        "Westlands", "Dagoretti North", "Dagoretti South",
        "Lang'ata", "Kibra", "Roysambu",
        "Kasarani", "Ruaraka", "Embakasi South",
        "Embakasi North", "Embakasi Central",
        "Embakasi East", "Embakasi West",
        "Makadara", "Kamukunji", "Starehe", "Mathare"
    ]
}


kenya_counties = [
    "Baringo", "Bomet", "Bungoma", "Busia", "Elgeyo Marakwet",
    "Embu", "Garissa", "Homa Bay", "Isiolo", "Kajiado",
    "Kakamega", "Kericho", "Kiambu", "Kilifi", "Kirinyaga",
    "Kisii", "Kisumu", "Kitui", "Kwale", "Laikipia",
    "Lamu", "Machakos", "Makueni", "Mandera", "Marsabit",
    "Meru", "Migori", "Mombasa", "Murang'a", "Nairobi",
    "Nakuru", "Nandi", "Narok", "Nyamira", "Nyandarua",
    "Nyeri", "Samburu", "Siaya", "Taita Taveta", "Tana River",
    "Tharaka Nithi", "Trans Nzoia", "Turkana", "Uasin Gishu",
    "Vihiga", "Wajir", "West Pokot"
]


class County(models.Model):
    title = models.CharField(max_length=30,unique=True)

    is_county = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.title.capitalize()}'
    
class Constituency(models.Model):
    title = models.CharField(max_length=30,unique=True)
    county = models.ForeignKey(County,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title.capitalize()}'
    
class Language(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.title.capitalize()}'
    
class Specialization(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.title.capitalize()}'
    
class EmploymentType(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.title.capitalize()}'
    
employment_choices = (
    ('Full Time','Full Time'),
    ('Contract','Contract'),
    ('B.O.M','B.O.M'),
    ('P.T.A','P.T.A'),
    ('Substitute','Substitute')
)

def createCountynConstituencies():
    County = apps.get_model('main','County')
    if (len(County.objects.all()) < 47 or len(County.objects.all()) > 47)and(len(Constituency.objects.all()) < 290 or len(Constituency.objects.all()) > 290) :
        for county in kenya_constituencies.keys():
            new_county = County.objects.create(title = county).save()
        for county in kenya_constituencies.keys():
            new_county = County.objects.get(title = county)
            for constituency in kenya_constituencies.get(county):
                Constituency.objects.create(county = new_county,title=constituency).save()


    # create constituencies
