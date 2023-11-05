from django.views.generic import FormView,TemplateView
from .forms import LoginForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
import os,json,time
from dotenv import load_dotenv
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from utils.common import makePostCall,set_cookies,logout_post_call,get_cookies
from django.contrib import messages
from apps.account import service as account_service


load_dotenv()
env = os.getenv

class LoginView(FormView):
    template_name = "auth/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('job:home')

    def call_login_api(self,data):
        base_url=env('BASE_URL') + 'accounts/login/'
        payload = json.dumps(data)
        res = makePostCall(base_url,payload)
        status_code = res.status_code
        if status_code == 500:
            return "Oops! something went wrong"
        
        elif status_code != 200:
            msg = json.loads(res.text)
            return msg['msg']
        
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return ""
    

    def form_invalid(self,form):
        msgs = []
        for error in form.errors.values():
            msgs.append(error.as_text())
        clean_msgs = [m.replace('* ', '') for m in msgs if m.startswith('* ')]
        messages.error(self.request, ",".join(clean_msgs))
        return super(LoginView, self).form_invalid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        request_dict = {
            'username' : data['username'],
            'password' : data['password']
        }
        res = self.call_login_api(request_dict)
        print(res)
        if type(res) != dict:
            messages.error(self.request, res,extra_tags='auth_msg')

            return HttpResponseRedirect('/auth/login')
        token = res['response']['token']
        response = HttpResponseRedirect(self.success_url)
        response = set_cookies(response,token)
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

class LogoutView(TemplateView):
    success_url = reverse_lazy('job:home')

    def logout_api_call(self, data):
        # access_token = f"Bearer {access_token}"
        base_url = env('BASE_URL') + 'accounts/logout/'
        payload =json.dumps( data)
        res = logout_post_call(base_url, payload)
        status_code = res.status_code

        if status_code == 500:
            return "Oops! Something went wrong"
        elif status_code == 401:
            return 401
        elif status_code != 200:
            msg = json.loads(res.text)
            return msg['msg']
        elif status_code == 200:
            data = json.loads(res.text)
            return data

        return ""
    def post(self, request, *args, **kwargs):
        self.access_token, self.refresh_token = get_cookies(request)
        if not self.access_token:
            return HttpResponseRedirect('/auth/login')

        refresh_token = self.refresh_token
        data = {
            'refresh': refresh_token,
        }
        res = self.logout_api_call(data)

        if res == 401:
            refresh_res = self.handle_refresh_token()
            if refresh_res:
                res = self.logout_api_call(data)
            if isinstance(res, str):
                return JsonResponse({'status': 'error', 'msg': res, 'res': {}})
        return JsonResponse({'status': 'success', 'msg': '', 'res': res})

    def handle_refresh_token(self):
        payload = {
            "refresh": self.refresh_token
        }
        api_res = account_service.call_refresh_api(payload)

        if isinstance(api_res, dict):
            token = api_res['response']
            self.access_token = token['access_token']
            self.refresh_token = token['refresh_token']
            self.is_set = True
            return True

        return False
