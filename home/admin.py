from django.contrib import admin
from .models import Profile, Item, Uploads, Downloads, Liked

class ProfileFields(admin.ModelAdmin):
    list_display= ('username', 'email', 'is_email_verified')

class ItemFields(admin.ModelAdmin):
    list_display= ('item_id', 'uuid', 'category', 'subcategory', 'likes', 'downloads_count', 'in_search')

admin.site.register(Profile, ProfileFields)
admin.site.register(Item, ItemFields)
admin.site.register(Uploads)
admin.site.register(Downloads)
admin.site.register(Liked)