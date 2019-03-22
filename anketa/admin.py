from django.contrib import admin
from .models import Organization,Partner,Offer,Anketa,Bid


class OfferAdmin(admin.ModelAdmin):
    readonly_fields = ('create', 'update')
    search_fields = ('name',)
    raw_id_fields = ('credit',)
    list_filter = ('status',)
    list_display = ('id', 'name', 'create', 'update', 'start_rotation', 'stop_rotation', 'min_ball', 'max_ball', 'credit', 'status')

class AnketaAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    raw_id_fields = ('partner',)
    list_filter = ('partner',)
    list_display = ('id', 'name', 'surname', 'first_name', 'Birthdate','telefon', 'pasport', 'ball', 'partner')

class BidAdmin(admin.ModelAdmin):
    readonly_fields = ('create',)
    search_fields = ('anketa',)
    raw_id_fields = ('anketa','offer')
    list_filter = ('status',)
    list_display = ('id', 'create', 'sent', 'anketa', 'offer', 'status')

admin.site.register(Organization)
admin.site.register(Partner)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Anketa, AnketaAdmin)
admin.site.register(Bid, BidAdmin)
