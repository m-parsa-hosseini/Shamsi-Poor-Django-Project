from django.contrib import admin
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	
from django.contrib.auth.admin import UserAdmin
from .models import User, User_info, User_absence, Register_absence, RegisterAbsenceDate, AbsenceRequestModel

   
admin.site.register(User, UserAdmin)
admin.site.register(AbsenceRequestModel)




@admin.register( User_info)
class UserInfoAdmin(admin.ModelAdmin):
    def full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)
    
    
    list_display =  ("user", "full_name", "pesonal_code", "national_code", "publish_at",)
    
@admin.register(User_absence)
class UserAbsenceAdmin(admin.ModelAdmin):
    list_display =  ("user",  "year",  "remaining_absence", )

@admin.register(Register_absence)
class Register_absenceAdmin(admin.ModelAdmin):
    pass



@admin.register(RegisterAbsenceDate)
class RegisterAbsenceDateAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
   
    @admin.display(description='تاریخ مرخصی', ordering='absence_date')
    def jalali_year(self, obj):
        return datetime2jalali(obj.absence_date).strftime('%Y/%m/%d')
    list_display =  ("user",  "jalali_year" ,"year")
    readonly_fields=('year', )



