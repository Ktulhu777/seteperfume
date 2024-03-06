from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

admin.site.register(User, UserAdmin)
#@admin.register(User)
#class UserAdmin(admin.ModelAdmin):
    #fields = "__all__",
