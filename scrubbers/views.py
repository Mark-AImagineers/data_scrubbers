from django.shortcuts import render


## FUNCTIONS






## VIEWS

def index(request):
    return render(request, 'index.html')

def weather_scrubber(request):
    return render(request, 'weather_scrubber.html')

## NOTES


# Weather Location:
# National Capital Region - Manila: +14.5995° N, +120.9842° E
# Cordillera Administrative Region - Baguio: +16.4023° N, +120.5960° E
# Ilocos Region - Ilocos Norte (Laoag): +18.1960° N, +120.5927° E
# Cagayan Valley - Tuguegarao: +17.6131° N, +121.7269° E
# Central Luzon - San Fernando (Pampanga): +15.0382° N, +120.6890° E
# Calabarzon - Calamba: +14.2166° N, +121.1743° E
# Southwestern Tagalog Region (MIMAROPA) - Calapan: +13.4110° N, +121.1799° E
# Bicol Region - Legazpi: +13.1387° N, +123.7438° E
# Western Visayas - Iloilo: +10.7202° N, +122.5621° E
# Central Visayas - Cebu: +10.3157° N, +123.8854° E
# Eastern Visayas - Tacloban: +11.2500° N, +125.0000° E
# Zamboanga Peninsula - Pagadian: +7.8245° N, +123.4376° E
# Northern Mindanao - Cagayan de Oro: +8.4542° N, +124.6319° E
# Davao Region - Davao: +7.1907° N, +125.4553° E
# Soccsksargen - Koronadal: +6.5018° N, +124.8472° E
# Caraga - Butuan: +8.9475° N, +125.5406° E
# Bangsamoro - Cotabato: +7.2236° N, +124.2464° E

# Time - 8:00 AM to 10:00 PM