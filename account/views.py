from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import  reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import F
import jdatetime
from jalali_date import datetime2jalali
from .forms import (SignupForm, )
from .mixins import  RedirectUserLoggedInMixin, RedirectNoneSuperUserMixin
from .models import User_absence, RegisterAbsenceDate, AbsenceRequestModel

    
    
class Home(RedirectNoneSuperUserMixin, LoginRequiredMixin, ListView):
    template_name = "registration/home.html"
    model = User_absence
    
    def get_queryset(self):
        # return User_absence.objects.all().order_by('-year')
        # jalali_current_year =  datetime2jalali(datetime.now()).strftime('%Y')
        return User_absence.objects.all()
 
class UserChangeInformation(RedirectNoneSuperUserMixin, LoginRequiredMixin, UpdateView):
    template_name = "registration/profile.html"
    model = get_user_model()
    
    fields = ('first_name', 'last_name', "father_name", 'date_joined', 'username', 'last_login', "pesonal_code", "national_code", "telephone", "phone", "address",)
    success_url = reverse_lazy("accounts:home")
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        form.fields["date_joined"].disabled = True
        form.fields["last_login"].disabled = True   
        return form
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        user = get_user_model().objects.get(pk=self.kwargs.get('pk'))
        context["absence"] = User_absence.objects.filter(user = user)
        return context

class UserChangeAbsence(RedirectNoneSuperUserMixin, LoginRequiredMixin, UpdateView):
    template_name = "registration/change-absence.html"
    # model = User_absence
    fields = ('user', 'year', "remaining_absence")
    
    def get_success_url(self) -> str:
        return reverse_lazy("accounts:user-change-info", kwargs={'pk': self.kwargs.get('pk')}) 
    
    def get_object(self):
        user = get_user_model().objects.get(pk=self.kwargs.get('pk'))
        return get_object_or_404(User_absence, user= user, year= str(self.kwargs.get('year')))
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        form.fields["user"].disabled = True
        form.fields["year"].disabled = True
        return form


class Profile(LoginRequiredMixin, UpdateView):
    template_name = "registration/profile.html"
    model = get_user_model()
    
    fields = ('first_name', 'last_name', "father_name", 'date_joined', 'username', 'last_login', "pesonal_code", "national_code", "telephone", "phone", "address",)
    success_url = reverse_lazy("accounts:profile")
    def get_object(self):#in this case we dont need to write the pk in the urls
        return get_object_or_404(get_user_model(), id=self.request.user.id)

        
    def get_form(self, form_class=None):
        # if self.request.user.is_superuser:
        #     self.fields = ('first_name', 'last_name', "father_name", 'date_joined', 'username', 'last_login', "pesonal_code", "national_code", "telephone", "phone", "address",)
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            # Disable these fields
            form.fields["username"].disabled = True
            form.fields["first_name"].disabled = True
            form.fields["last_name"].disabled = True
            form.fields["father_name"].disabled = True
            form.fields["pesonal_code"].disabled = True
            form.fields["national_code"].disabled = True
            form.fields["date_joined"].disabled = True
            form.fields["last_login"].disabled = True
       
        return form
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["absence"] = User_absence.objects.filter(user=self.request.user)
        return context
    
class AbsenceRequest(LoginRequiredMixin, CreateView):
    ''' absence request by user '''
    template_name = "registration/absence-request.html"
    model = AbsenceRequestModel
    
    # fields = ('user', 'absence_date', "year", "status", "status_message")

    success_url = reverse_lazy("accounts:absence-request-list")


    def get_form(self, form_class=None):
        self.fields =  ( "year",  "month",  "day" , "absence_length")

        if self.request.user.is_superuser:
            self.fields = "__all__"
        form = super().get_form(form_class)
        # if not self.request.user.is_superuser:
            # Disable these fields
            # form.fields["user"].disabled = True
            # form.fields["status_message"].disabled = True
        return form
    
    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.user = self.request.user
        if  form.instance.status != "a" or form.instance.status != "d":
            form.instance.status = "w"


        if  self.request.user.is_superuser:
            if  form.instance.status == "a":
                for i in range(form.instance.absence_length):
                    gdate = jdatetime.datetime(form.instance.year, form.instance.month, form.instance.day).togregorian() + timedelta(days= i )
                    RegisterAbsenceDate.objects.create(user = form.instance.user, absence_date = gdate )
                # User_absence.objects.filter(user=form.instance.user, year=str( form.instance.year)).update(remaining_absence=F('remaining_absence')- form.instance.absence_length)
       
        if not AbsenceRequestModel.objects.filter( user= self.request.user , year= int(form.instance.year), month= int( form.instance.month), day= int( form.instance.day)).exists(): #if query does not exist
            return super().form_valid(form)
        return redirect(reverse('accounts:absence-request-list'))
    
        
    

class AbsenceRequestUpdate(LoginRequiredMixin, UpdateView):
    ''' absence request by user '''
    template_name = "registration/absence-request.html"
    model = AbsenceRequestModel
    
    fields = "__all__"

    success_url = reverse_lazy("accounts:absence-request-list")

    def get_object(self):
        user = get_user_model().objects.get(pk=self.kwargs.get('user_pk'))
        return get_object_or_404(AbsenceRequestModel, user= user, year= int(self.kwargs.get('year')), month= int(self.kwargs.get('month')), day= int(self.kwargs.get('day')))
    
    def form_valid(self, form):
        if  form.instance.status not in ['w', 'a', 'd']:
            form.instance.status = "w"

        # jalali_year =  datetime2jalali(instance.absence_date).strftime('%Y')
        # instance.year = int(jalali_year)
        if  form.instance.status == "a":
            for i in range(form.instance.absence_length):
                gdate = jdatetime.datetime(form.instance.year, form.instance.month, form.instance.day).togregorian() + timedelta(days= i )
                if not RegisterAbsenceDate.objects.filter(user = form.instance.user, absence_date = gdate ).exists():
                    RegisterAbsenceDate.objects.create(user = form.instance.user, absence_date = gdate )
        # User_absence.objects.filter(user=form.instance.user, year=str( form.instance.year)).update(remaining_absence=F('remaining_absence')- form.instance.absence_length)
        return super().form_valid(form)
    
    # def dispatch(self, request, *args, **kwargs):
        
    #     if not request.user.is_superuser:
    #         redirect(reverse("accounts:profile"))
    #     return super().dispatch(request, *args, **kwargs)

class AbsenceRequestList(LoginRequiredMixin, ListView):
    ''' absence request by user '''
    template_name = "registration/absence-request-list.html"
    model = AbsenceRequestModel
    
    fields = "__all__"

    def get_queryset(self) :
        if  self.request.user.is_superuser:
            query =  AbsenceRequestModel.objects.all()
        else : 
            query =  AbsenceRequestModel.objects.filter(user=self.request.user)
        return query

class AbsenceRequestDelete(LoginRequiredMixin, DeleteView):
    model = AbsenceRequestModel
    success_url = reverse_lazy("accounts:absence-request-list")
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super().get_object()
        if ( obj.user == self.request.user and obj.status == "w") or  self.request.user.is_superuser:
            return obj
        return redirect(reverse("accounts:absence-request-list"))
    


class RegisterAbsenceDateView(LoginRequiredMixin, ListView):
    ''' absence request by user '''
    template_name = "registration/absence-date.html"
    # model = RegisterAbsenceDate
    fields = ('user', 'absence_date', "year")
    
    def get_success_url(self) -> str:
        return reverse_lazy("accounts:user-change-info", kwargs={'pk': self.kwargs.get('pk')}) 
    
        
    def get_queryset(self) :
        user = get_user_model().objects.get(pk=self.kwargs.get('pk'))
        return RegisterAbsenceDate.objects.filter(user=user, year= int(self.kwargs.get('year')))
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["user"].disabled = True
        form.fields["year"].disabled = True
        form.fields["absence_date"].disabled = True
        return form


class Register(RedirectUserLoggedInMixin,CreateView):
    template_name = "registration/signup.html"
    redirect_authenticated_user = True
    form_class = SignupForm
    def get_success_url(self) -> str:
        return self.request.GET.get('next',reverse("accounts:profile"))
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get('next')
        return context
    
    ## in case of auto Login
    def form_valid(self, form):
        # save the new user first
        form.save()
        # user = form.save(commit=False)
        # user.set_password(form.cleaned_data.get("password1"))
        # user.save()
        
        # get the username and password
        # username = self.request.POST['username']
        username  = form.cleaned_data['username']
        password =  form.cleaned_data['password1']
        # authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(reverse("accounts:profile"))


class CustomLogoutView(LogoutView):
    def get_success_url(self):
        return reverse("accounts:login")
    
class Login(LoginView):
    pass
    # def get_success_url(self):
    #     if not self.request.user.is_author:
    #         return reverse("accounts:profile")
    #     else:
    #         return reverse("accounts:home")


class CustomPasswordChangeView(PasswordChangeView):

    def get_success_url(self):
        messages.success(self.request, 'پسورد شما با موفقیت تغییر پیدا کرد')
        return reverse("accounts:profile")
