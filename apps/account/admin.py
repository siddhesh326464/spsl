from django.contrib import admin
from apps.account.models import AbstractUser
from apps.account.models import Account
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display=('id','email','username','rep_no','role','status','contact_no','first_name','last_name')
    list_filter=('id','email')
    fieldsets=(
        ('User credential', {'fields': ('username', 'password')}),
        ('personal info',{'fields':('email','rep_no','role','status','contact_no','first_name','last_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets=(
        (None,{
            'classes': ('wide',),
            'fields': ('email','username','rep_no','role','status','contact_no','first_name','last_name','password1','password2')
        }),
    )
    search_fields=('email','username',)
    ordering = ('id',)
    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['first_name'].required = True
        form.base_fields['last_name'].required = True
        return form
                                                                                                                                                                        

admin.site.register(Account, UserModelAdmin)