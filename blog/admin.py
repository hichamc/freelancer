from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from .models import Project, Bid, Account, Review, Category, Pimage


admin.site.register(Project)
admin.site.register(Bid)
# admin.site.register(Account, UserAdmin)
admin.site.register(Account)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Pimage)