from django import template
from Bloger import models
regester = template.Library()
@regester.inclusion_tag('Bloger/AllAds.html')
def AllAdd():
    context = {
        'AllAd_l':models.newAd.objects.all()
    }
    return context