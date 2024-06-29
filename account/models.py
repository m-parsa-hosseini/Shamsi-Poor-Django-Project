from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from datetime import datetime
from jalali_date import datetime2jalali
from django.db.models import F
from django.core.validators import MaxValueValidator, MinValueValidator

def generate_11_digit():
    return get_random_string(11, allowed_chars='0123456789') 

class User(AbstractUser):
    father_name = models.CharField(max_length=30, default='', verbose_name='نام پدر',)
    pesonal_code = models.CharField(max_length=11, unique=True, default=generate_11_digit, verbose_name='کدکارمندی',help_text="۱۱ رقم")
    national_code = models.CharField(max_length=11,verbose_name='کد ملی', unique=True, default=generate_11_digit, help_text="۱۱ رقم")
    telephone = models.CharField(max_length=8, default='', verbose_name="خط ثابت", help_text="8 رقم")
    phone = models.CharField(max_length=11, default='', verbose_name="شماره تلفن", help_text="۱۱ رقم")
    address = models.TextField(default='', verbose_name="آدرس")
    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'




class User_info(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='user_info')
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=150, default='')
    father_name = models.CharField(max_length=30, default='')
    pesonal_code = models.CharField(max_length=11, unique=True, default=generate_11_digit)
    national_code = models.CharField(max_length=30,verbose_name='کد ملی', unique=True, default=generate_11_digit)
    telephone = models.CharField(max_length=8, default='')
    phone = models.CharField(max_length=11, default='')
    address = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ استخدام شدن")
    updated_at = models.DateTimeField(auto_now=True)
    publish_at = models.DateTimeField(blank=True, default=timezone.now,  verbose_name="تاریخ استخدام شدن" )
    
    def __str__(self):
        return str(self.user)
    class Meta:
        verbose_name = 'پروفایل کاربر '
        verbose_name_plural = 'پروفایل کاربر ها '

class User_absence(models.Model):
    STATUS = [
    ("1403" , "1403"),
    ("1404" , "1404"),
    ("1405" , "1405"),
    ("1406" , "1406"),
    ("1407" , "1407"),
    ("1408" , "1408"),
    ("1409" , "1409"),
    ("1410" , "1410"),
    ("1411" , "1411"),
    ("1412" , "1412"),
    ("1413" , "1413"),
    ("1414" , "1414"),
    ("1415" , "1415"),
    ("1416" , "1416"),
    ("1417" , "1417"),
    ("1418" , "1418"),
    ("1419" , "1419"),
    ("1420" , "1420"),
]
    
    user =  models.ForeignKey(get_user_model(), verbose_name=("کارمند"),on_delete=models.CASCADE, related_name="absences")
    year =  models.CharField(("سال"),choices=STATUS, max_length=4)
    remaining_absence = models.IntegerField(("مرخصی های باقی مانده"), default=30)
    # last_year_remain_absence = models.IntegerField()
    def __str__(self):
        return str(self.user)
    class Meta:
        verbose_name = 'تعداد مرخصی کارمند'
        verbose_name_plural = 'تعداد مرخصی کارمندها'
    
class Register_absence(models.Model):

    year =  models.IntegerField((" سال به شمسی"), help_text="مثال :‌1403", unique=True)
    
    def __str__(self):
        return str(self.year)
    class Meta:
        verbose_name = 'ثبت مرخصی کارمند در ابتدا سال  '
        verbose_name_plural = 'ثبت مرخصی کارمندها در ابتدا سال  '

class RegisterAbsenceDate(models.Model):
    
    user =  models.ForeignKey(get_user_model(), verbose_name=("کارمند"),on_delete=models.CASCADE, related_name="absence_date")
    absence_date = models.DateTimeField(default=timezone.now,  verbose_name="تاریخ مرخصی" )
    year = models.IntegerField(null=True, blank=True, verbose_name="سال")#readonlyField
    
    def __str__(self):
        return str(self.user)
    class Meta:
        verbose_name = ' ثبت مرخصی'
        verbose_name_plural = ' ثبت مرخصی ها'
    

class AbsenceRequestModel(models.Model):
    STATUS = [
    ("a" , "تایید"), #accept
    ("d" , "رد"), #deny
    ("w" , "در انتظار"), # waitng
]
    user =  models.ForeignKey(get_user_model(), verbose_name=("کارمند"),on_delete=models.CASCADE, related_name="absence_request")

    year = models.IntegerField(null=True, blank=True, verbose_name="سال", default= int(datetime2jalali(datetime.now()).strftime('%Y')))
    month = models.IntegerField(null=True, blank=True, verbose_name="ماه",default= int(datetime2jalali(datetime.now()).strftime('%m')),  validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ])
    day = models.IntegerField(null=True, blank=True, verbose_name="روز", default= int(datetime2jalali(datetime.now()).strftime('%d')), validators=[
            MaxValueValidator(31),
            MinValueValidator(1)
        ])
    absence_length = models.IntegerField(verbose_name="طول مرخصی", default=1)
    status =  models.CharField(("وضعیت"),choices=STATUS, max_length=10, default="w")
    status_message =  models.TextField(("پیام مورد نظر برای تایید یا رد"),null=True, blank=True,)
    
    def __str__(self):
        return str(self.user)
    class Meta:
        verbose_name = ' ثبت مرخصی توسط کاربر'
        verbose_name_plural = ' ثبت مرخصی توسط کاربر ها '

@receiver(post_save, sender=get_user_model())
def create_user_info_and_absence(sender, instance, created, **kwargs):
    if created:
        User_info.objects.create(user = instance)
        jalali_current_year =  datetime2jalali(datetime.now()).strftime('%Y')
        User_absence.objects.get_or_create(user = instance, year  = jalali_current_year )
    
@receiver(pre_save, sender=RegisterAbsenceDate)
def create_user_absence_with_date(sender, instance, **kwargs):
        jalali_year =  datetime2jalali(instance.absence_date).strftime('%Y')
        instance.year = int(jalali_year)
        User_absence.objects.filter(user=instance.user, year=str(jalali_year)).update(remaining_absence=F('remaining_absence')-1)
        
    
@receiver(post_save, sender=Register_absence)
def update_users_absence(sender, instance, **kwargs):
    
    for user in get_user_model().objects.all():
        
        User_absence_is_exist = User_absence.objects.filter(user = user, year = str(instance.year)).exists()
        if not User_absence_is_exist:
            this_year_user_absence = User_absence.objects.create(user = user, year = str(instance.year), remaining_absence = 30)
        last_year_remaining = user.absences.filter(year=str(instance.year -1 ))
        
        if(last_year_remaining):
            # print(">>>>>>>>>>>>>>>>",user.absences.filter(year=str(instance.year -1 )).first())
            last_year_remaining_absence = last_year_remaining.first().remaining_absence
            if last_year_remaining_absence >= 7   :
                this_year_user_absence.remaining_absence += 7
            elif last_year_remaining_absence < 7:
                this_year_user_absence.remaining_absence += last_year_remaining_absence
                
        if not User_absence_is_exist:     
            this_year_user_absence.save()
            
    # instance.product.save()

