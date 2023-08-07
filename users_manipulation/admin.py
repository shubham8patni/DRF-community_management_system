from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser
# Register your models here.

class MyUserAdmin(UserAdmin):
        
    model = MyUser
    list_display = ('mobile_number', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
    fieldsets = (
        ('Credentials', {'fields': ('mobile_number', 'password')}),
        ('User Info', {'fields': ('first_name', 'last_name')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
        ('Pernissions', {'fields': ('is_staff','is_active')}),
        ('Groups and Permissions', {'fields' : ('groups','user_permissions')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'password1', 'password2', 'groups', 'is_staff', 'is_active'),
        }),
    )
    
    search_fields = ('mobile_number',)
    ordering=('date_joined',)


admin.site.register(MyUser, MyUserAdmin)
