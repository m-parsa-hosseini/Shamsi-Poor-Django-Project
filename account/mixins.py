from django.urls import  reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect


class RedirectNoneSuperUserMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect(reverse("accounts:profile"))
        return super().dispatch(request, *args, **kwargs)
        
class RedirectUserLoggedInMixin(object):
    redirect_authenticated_user = False
    def dispatch(self, request , *args, **kwargs) :
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            return redirect(redirect_to)
            
        return super().dispatch(request, *args, **kwargs)