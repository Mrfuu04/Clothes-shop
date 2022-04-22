from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View, ContextMixin


class AdminContextMixin(ContextMixin):
    title = ''

    def get_context_data(self, **kwargs):
        context = super(AdminContextMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class SuperuserDispatchMixin(View):

    @method_decorator(user_passes_test(lambda u: u.is_superuser, login_url='/login'))
    def dispatch(self, request, *args, **kwargs):
        return super(SuperuserDispatchMixin, self).dispatch(request, *args, **kwargs)




class AuthorisationDispatchMixin(View):

    @method_decorator(login_required(login_url='/login'))
    def dispatch(self, request, *args, **kwargs):
        return super(AuthorisationDispatchMixin, self).dispatch(request, *args, **kwargs)
