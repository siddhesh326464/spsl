import os,json,boto3
from datetime import datetime
from typing import Any, Dict
from django import http
from django.db import models
from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.generic import TemplateView,CreateView,DetailView,UpdateView
from apps.job.models import Job,Campaign,Jobitem,SubmittedFiles,CompletedFiles,EpsFiles,LogoFiles,JobLog
from utils.constant import JOB_STATUS,PROOF_TYPE
from dotenv import load_dotenv
from utils.common import makeGetCall,get_cookies,set_cookies,makePostCall,makePutCall,makeJobPutCall,sendmsg_post_call,campaign_post_api,deletefile_put_api
from apps.account import service as account_service
from .forms import CreateJobForm,UpdateJobForm,UpdateJobItemForm,JobUpdateItemFormSet
from django.urls import reverse_lazy
from django.contrib import auth, messages
from api.account.views import CommonUserMixins
from api.email_templates import *
from utils.notify import send_email
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import zipfile
import io
from io import BytesIO
import asyncio
import contextlib
# from django.core.exceptions import SMTPException
import smtplib

load_dotenv()
env = os.getenv

class JobView(TemplateView,CommonUserMixins):
    template_name = 'jobs/index.html'
    access_token = None
    refresh_token = None
    is_set = False
   
    def get(self, request, *args, **kwargs):
        self.access_token,self.refresh_token = get_cookies(request)
        if not self.access_token:
            return HttpResponseRedirect('/auth/login')
        res = super().get(request, *args, **kwargs)
        return res
    
    def call_get_api(self,access_token):
        access_token = f"Bearer {access_token}"
        base_url=env('BASE_URL') + 'jobs/alljobs/'
        res = makeGetCall(base_url,{},access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops! something went wrong"

        elif status_code == 401:
            return 401
                
        elif status_code != 200:
            msg = json.loads(res.text)
            return msg['msg']
        
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return ""
    
    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        if self.is_set:
            token = {
                'access' : self.access_token,
                'refresh' : self.refresh_token
            }
            response = set_cookies(response,token)
            self.is_set = False
        return response
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status'] = JOB_STATUS
        ctx['status_name'] = [s['name'].lower() for s in JOB_STATUS]
        ctx['user'] = self.get_user(self.request)
        res = self.call_get_api(self.access_token)
        if res == 401:
            payload = {
                "refresh":self.refresh_token
            }
            api_res = account_service.call_refresh_api(payload)
            if type(api_res) == dict:
                token = api_res['response']
                self.access_token = token['access_token']
                self.refresh_token = token['refresh_token']
                res = self.call_get_api(self.access_token)
                self.is_set = True
        if type(res) != dict:
            res = []
            total_count = {}
        else:
            total_count = res['response'].pop('total_count')
            res = res['response']

        ctx['total_count'] = total_count
        ctx['jobs'] = res
        return ctx
    
class CreateJobView(CreateView,CommonUserMixins):
    model = Job
    form_class = CreateJobForm
    # other_form_class = JobItemForm
    template_name = "jobs/create_job.html"
    success_url = reverse_lazy("job:home")
    current_url = reverse_lazy("job:createjob")
    access_token = None
    refresh_token = None
    is_set = False
    user = None
   
    def get(self, request, *args, **kwargs):
        self.access_token,self.refresh_token = get_cookies(request)
        if not self.access_token:
            return HttpResponseRedirect('/auth/login')
        res = super().get(request, *args, **kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        return self.render_to_response(
            self.get_context_data(form=form))
    
    def get_initial(self):
        initial = super().get_initial()
        self.user = self.get_user(self.request)
        initial = {
            "user_email" : self.user.email,
            "rep_no": f"{self.user.first_name} {self.user.last_name} - {self.user.rep_no}",
            "status" : "New"
        }
        return initial
    
    # This is dispach method for Campaign

    def call_campaign_api(self,data,access_token):
        access_token = f"Bearer {access_token}"
        base_url=env('BASE_URL') + 'jobs/createcampaign/'
        payload = data
        res = campaign_post_api(base_url,payload,access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops! something went wrong"

        elif status_code == 401:
            return 401
                
        elif status_code != 200:
            msg = json.loads(res.text)
            return msg['msg']
        
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return "" 
    

    def dispatch(self, request ,*args, **kwargs):
        if request.method == 'POST' and request.POST.get('name',None):
            self.access_token,self.refresh_token = get_cookies(request)
            if not self.access_token: 
                return HttpResponseRedirect('/auth/login')
            id = request.POST.get('id',None)
            data = {
                'id':id,
                'name':request.POST['name']
            }
            
            res = self.call_campaign_api(data,self.access_token)
            if res == 401:
                refresh_res = self.handel_refresh_token()
                if refresh_res:
                    res = self.call_campaign_api(data,self.access_token)
            if type(res) == str:
                return JsonResponse({'status':'error','msg':res,'res':{}})
            return JsonResponse({'status':'success','msg':'','res':res['response']})
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.access_token,self.refresh_token = get_cookies(request)
        if not self.access_token:
             return HttpResponseRedirect('/auth/login')
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        jobitem_form = CreateJobForm(self.request.POST,self.request.FILES)
        if (form.is_valid() and jobitem_form.is_valid()):
            return self.form_valid(form, jobitem_form)
        else:
            return self.form_invalid(form,jobitem_form)
        
    def form_invalid(self,form,jobitem_form):
        msgs = []
        for error in form.errors.values():
            msgs.append(error.as_text())
        clean_msgs = [m.replace('* ', '') for m in msgs if m.startswith('* ')]
        messages.error(self.request, ",".join(clean_msgs))
        # return super(CreateJobView, self).form_invalid(form,jobitem_form)
        files = jobitem_form.files
        return self.render_to_response(
            self.get_context_data(form=form,
                                  jobitem_form=jobitem_form,files=files))

    def createjob_call_api(self,data,access_token):
        access_token = f"Bearer {access_token}"
        base_url=env('BASE_URL') + 'jobs/addjob/'
        payload =json.dumps(data)
        res = makePostCall(base_url,payload,access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops something went wrong"
        elif status_code == 401:
            return 401
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return ""

    def createjobitem_call_api(self,data,access_token):
        access_token = f"Bearer {access_token}"
        base_url=env('BASE_URL') + 'jobs/createjobitem/'
        payload =json.dumps(data)
        res = makePostCall(base_url,payload,access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops something went wrong"
        elif status_code == 401:
            return 401
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return ""

    def upload_file_api(self,sub_file,item_id):
        access_token = f"Bearer {self.access_token}"
        base_url = env('BASE_URL')+'jobs/uploadfile/'
        files = [
                ('file', (file.name, file.read(), file.content_type))
                for file in sub_file
            ]
        payload = {"file_type": "1","item_id": item_id}
        res = makePutCall(base_url,payload,files,access_token)
    
    def handel_refresh_token(self):
        payload = {
                    "refresh":self.refresh_token
                }
        api_res = account_service.call_refresh_api(payload)
        if type(api_res) == dict:
            token = api_res['response']
            self.access_token = token['access_token']
            self.refresh_token = token['refresh_token']
            self.is_set = True
            return True
        return False

    def form_valid(self, form,jobitem_form):
        try:
            quote_no = form.cleaned_data['quote_no']
            logo_name = form.cleaned_data['logo_name']
            logo_same_for_all = form.cleaned_data['logo_same_for_all']
            logo_same_for_all = True if logo_same_for_all == 'True' else False
            send_art_to_customer = form.cleaned_data['send_art_to_customer']
            send_art_to_customer = True if send_art_to_customer == 'True' else False
            proof_request_type = form.cleaned_data['proof_request_type']
            customer_no = form.cleaned_data['customer_no']
            customer_email = form.cleaned_data['customer_email']
            customer_name = form.cleaned_data['customer_name']
            segment_no = form.cleaned_data['segment_no']
            campaign = form.cleaned_data['campaign'].id if form.cleaned_data['campaign'] else None
            rep_no = form.cleaned_data['rep_no']
            status = "1"
            note = form.cleaned_data['note']
            item = form.cleaned_data['item']
            product_color = form.cleaned_data['product_color']
            imprint_color = form.cleaned_data['imprint_color']
            imprint_location = form.cleaned_data['imprint_location']
            imprint_method = form.cleaned_data['imprint_method']
            imprint_instructions = form.cleaned_data['imprint_instructions']
            submitted_files = form.cleaned_data['submitted_files']
            jobitem_data = jobitem_form.cleaned_data
            job_data={
                "quote_no": quote_no,
                "logo_name":logo_name ,
                "logo_same_for_all":logo_same_for_all ,
                "send_art_to_customer":send_art_to_customer,
                "proof_request_type": proof_request_type,
                "campaign":campaign,
                "customer_no":customer_no,
                "customer_email":customer_email,
                "customer_name": customer_name,
                "segment_no":segment_no ,
                "rep_no":rep_no ,
                "note":note ,
                "status":status,
                "item": item,
                "product_color":product_color,
                "imprint_color":imprint_color,
                "imprint_location":imprint_location,
                "imprint_method": imprint_method,
                "imprint_instructions":imprint_instructions ,
                "submitted_files":submitted_files ,
                
            }
            job_create_data_addjob = {
                    "quote_no": quote_no,
                "logo_name": logo_name,
                "logo_same_for_all": logo_same_for_all,
                "send_art_to_customer": send_art_to_customer,
                "proof_request_type": proof_request_type,
                "campaign": campaign,
                "customer_no": customer_no,
                "customer_email":customer_email,
                "customer_name": customer_name,
                "segment_no": segment_no,
                "note": note,
                "status": status,
                "item": [
                    {
                        "item": item,
                        "product_color": product_color,
                        "imprint_color": imprint_color,
                        "imprint_location": imprint_location,
                        "imprint_method": imprint_method,
                        "imprint_instructions": imprint_instructions,
                    }
                ]
            }
            sub_files = job_data.pop('submitted_files')
            res = self.createjob_call_api(job_create_data_addjob,self.access_token)
            if res == 401:
                refresh_res = self.handel_refresh_token()
                if refresh_res:
                    res = self.createjob_call_api(job_create_data_addjob,self.access_token)

            item_id = res['response']['job'][0]['id']
            job_id = res['response']['id']
            res = self.upload_file_api(sub_files,item_id)
            if res ==401:
                refresh_res = self.handel_refresh_token()
                if refresh_res:
                    res = self.upload_file_api(sub_files,item_id)
            # if type(res) != dict:
            #     messages.error(self.request, res,extra_tags='job_msg')
            # job_id = res['response']['id']
            # for form_index, form in enumerate(jobitem_form):
            #     try:
            #         prefix = f"{form.prefix}-submitted_files"
            #         job_item_dict = form.cleaned_data
            #         job_item_dict.pop('submitted_files')
            #         job_item_dict.pop('id')
            #         job_item_dict['job_id_id'] = job_id
            #         res = self.createjobitem_call_api(job_item_dict,self.access_token)
            #         if res == 401:
            #             refresh_res = self.handel_refresh_token()
            #             if refresh_res:
            #                 res = self.createjobitem_call_api(job_item_dict,self.access_token)
            #         if type(res) != dict:
            #             messages.error(self.request, res,extra_tags='job_msg')
            #         item_id = res['response']['id']
            #         submitted_files  = self.request.FILES.getlist(prefix)
            #         # submitted_files =submittedfile(f"{form.prefix}-submitted_files")
            #         res = self.upload_file_api(submitted_files,item_id)
            #         if res == 401:
            #             refresh_res = self.handel_refresh_token()
            #             if refresh_res:
            #                 res = self.upload_file_api(submitted_files,item_id)
            #     except Exception as e:
            #         print(e)
            
            data={
                'subject':NEW_JOB_SUBJECT.format(job_id,quote_no),
                'body':NEW_JOB_BODY.format(job_id,env('CLIENT_NAME')),
                'to_email':self.user.email,
                'cc':env('EMAIL_CC').split(',')
                }
            send_email(data)
            messages.success(self.request, 'Job has been created successfully.', extra_tags='job_msg')
            response = HttpResponseRedirect(self.success_url)
            if self.is_set:
                token = {
                    'access' : self.access_token,
                    'refresh' : self.refresh_token
                }
                response = set_cookies(response,token)
                self.is_set = False
            return response
        except Exception as e:
            print(e)
            return HttpResponseRedirect(self.current_url)

    def get_context_data(self, **kwargs):
        ctx = super(CreateJobView,self).get_context_data(**kwargs)
        ctx['contact_title'] = "Add Contact"
        ctx['action'] = 'ADD'
        ctx['user'] = self.get_user(self.request)
        return ctx

class JobDetailview(DetailView,CommonUserMixins):
    model = Job
    template_name = 'jobs/jobdetail.html'
    form_class = CreateJobForm
    access_token = None
    refresh_token = None
    is_set = False
    id = None

    def get(self, request, *args, **kwargs):
        self.access_token,self.refresh_token = get_cookies(request)
        self.id = self.kwargs['pk']
        if not self.access_token:
            return HttpResponseRedirect('/auth/login')
        res = self.call_detail_api(self.access_token,self.id)
        if res == 401:
            payload = {
                "refresh":self.refresh_token
            }
            api_res = account_service.call_refresh_api(payload)
            if type(api_res) == dict:
                token = api_res['response']
                self.access_token = token['access_token']
                self.refresh_token = token['refresh_token']
                res = self.call_detail_api(self.access_token , self.id)
                self.is_set = True
        if type(res) == str:
            return HttpResponse(res)
        response = res['response']
        proof_key,proof_value = list(filter(lambda x:x[0] == response['proof_request_type'],PROOF_TYPE))[0]
        response['proof_request_type'] = {'proof_key':proof_key,'proof_value':proof_value}
        status = list(filter(lambda x:x['value'] == int(response['status']),JOB_STATUS))[0]
        response['status'] = {'status_key':status['value'],'status_value':status['name']}
        campaign_id = response['campaign']
        campign = Campaign.objects.filter(id = campaign_id).first()
        response['campaign'] = campign.name if campaign_id else ""
        messages = self.call_getmsg_api(self.access_token,self.id)
        if messages == 401:
            payload = {
                "refresh":self.refresh_token
            }
            api_res = account_service.call_refresh_api(payload)
            if type(api_res) == dict:
                token = api_res['response']
                self.access_token = token['access_token']
                self.refresh_token = token['refresh_token']
                messages = self.call_getmsg_api(self.access_token,self.id)
                self.is_set = True
        messages = [] if type(messages) == str else messages['response']
        return self.render_to_response({'jobdetail': response,'user':self.get_user(request),'msgs':messages})
    
    def handel_refresh_token(self):
        payload = {
                    "refresh":self.refresh_token
                }
        api_res = account_service.call_refresh_api(payload)
        if type(api_res) == dict:
            token = api_res['response']
            self.access_token = token['access_token']
            self.refresh_token = token['refresh_token']
            self.is_set = True
            return True
        return False
    
    def call_sendmsg_api(self,data,access_token,file):
        access_token = f"Bearer {access_token}"
        base_url=env('BASE_URL') + 'jobs/{}/sendmessages/'.format(self.id)
        res = sendmsg_post_call(base_url,data,file,access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops! something went wrong"

        elif status_code == 401:
            return 401
                
        elif status_code != 200:
            msg = json.loads(res.text)
            return msg['msg']
        
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return ""
       
    def dispatch(self, request ,*args, **kwargs):
        if request.method == 'POST':
            self.id = self.kwargs['pk']
            self.access_token,self.refresh_token = get_cookies(request)
            if not self.access_token:
                return HttpResponseRedirect('/auth/login')
            files = None
            if request.FILES:
                file=request.FILES.getlist('attachment')[0]
                files = [
                ('attachment', (file.name, file.read(), file.content_type))
            
            ]
            data ={
                'details':request.POST['details']
            }
            
            res = self.call_sendmsg_api(data,self.access_token,files)
            if res == 401:
                refresh_res = self.handel_refresh_token()
                if refresh_res:
                    res = self.call_sendmsg_api(data,self.access_token,files)
            return JsonResponse(res)
        if request.method == 'GET':
            self.id = self.kwargs['pk']
            self.access_token,self.refresh_token = get_cookies(request)
            if not self.access_token:
                return HttpResponseRedirect('/auth/login')
            if 'file_url' not in request.GET:
                return super(JobDetailview,self).dispatch(request, *args, **kwargs)
            file_url = request.GET['file_url']
            res = self.call_download_fileapi(self.access_token,file_url)
            if res == 401:
                refresh_res = self.handel_refresh_token()
                if refresh_res:
                    res = self.call_download_fileapi(file_url,self.access_token)
            return JsonResponse(res)
        return super().dispatch(request, *args, **kwargs)
    
    def call_getmsg_api(self,access_token,id):
        access_token = f"Bearer {access_token}"
        base_url=env('BASE_URL') + 'jobs/getjoblog/{}/'.format(id)
        res = makeGetCall(base_url,{},access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops! something went wrong"

        elif status_code == 401:
            return 401
                
        elif status_code != 200:
            msg = json.loads(res.text)
            return msg['msg']
        
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return ""

    def call_detail_api(self,access_token,id):
        access_token = f"Bearer {access_token}"
        base_url=env('BASE_URL') + 'jobs/jobdetail/{}/'.format(id)
        res = makeGetCall(base_url,{},access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops! something went wrong"

        elif status_code == 401:
            return 401
                
        elif status_code != 200:
            msg = json.loads(res.text)
            return msg['msg']
        
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return ""
    
    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        if self.is_set:
            token = {
                'access' : self.access_token,
                'refresh' : self.refresh_token
            }
            response = set_cookies(response,token)
            self.is_set = False
        return response
    
class UpdateJobView(UpdateView,CommonUserMixins):
    model = Job
    template_name = "jobs/update_job.html"
    form_class = UpdateJobForm
    success_url = reverse_lazy("job:home")
    current_url = reverse_lazy("job:appupdatejob")
    access_token = None
    refresh_token = None
    is_set = False
    model = Job
    pk = None
    user = None
    job_details = None
    
    
    def get(self, request, *args, **kwargs):
        self.access_token,self.refresh_token = get_cookies(request)
        if not self.access_token:
            return HttpResponseRedirect('/auth/login')
        res = super().get(request, *args, **kwargs)
        return res
    
    def get_object(self,queryset = None):
        return get_object_or_404(Job,id=self.kwargs['pk'])
    
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        self.access_token,self.refresh_token = get_cookies(request)
        if not self.access_token:
             return HttpResponseRedirect('/auth/login')
        form = self.form_class(self.request.POST)
        jobitem_form = JobUpdateItemFormSet(self.request.POST,self.request.FILES,instance=self.object)  
        if form.is_valid() and jobitem_form.is_valid():
            return self.form_valid(form,jobitem_form)
        else:
            return self.form_invalid(form,jobitem_form)
        
    def form_invalid(self,form,jobitem_form):
        msgs = []
        for error in form.errors.values():
            msgs.append(error.as_text())
        clean_msgs = [m.replace('* ', '') for m in msgs if m.startswith('* ')]
        messages.error(self.request, ",".join(clean_msgs))
        return self.render_to_response(
            self.get_context_data(form=form,
                                jobitem_form=jobitem_form))
    def call_campaign_api(self,data,access_token):
        access_token = f"Bearer {access_token}"
        base_url=env('BASE_URL') + 'jobs/createcampaign/'
        payload = data
        res = campaign_post_api(base_url,payload,access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops! something went wrong"

        elif status_code == 401:
            return 401
                
        elif status_code != 200:
            msg = json.loads(res.text)
            return msg['msg']
        
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return "" 
    def call_delete_file_api(self,data,access_token,file_id):
        access_token = f"Bearer {access_token}"
        base_url=env('BASE_URL') + 'jobs/deletefile/'+'{}/'.format(file_id)
        payload = data
        res =deletefile_put_api(base_url,payload,access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops! something went wrong"

        elif status_code == 401:
            return 401
                
        elif status_code != 200:
            msg = json.loads(res.text)
            return msg['msg']
        
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return "" 

    def dispatch(self, request ,*args, **kwargs):
        self.id = self.kwargs['pk']
        if request.method == 'POST' and request.POST.get('name',None):
            self.access_token,self.refresh_token = get_cookies(request)
            if not self.access_token: 
                return HttpResponseRedirect('/auth/login')
            id = request.POST.get('id',None)
            data = {
                'id':id,
                'name':request.POST['name']
            }
            
            res = self.call_campaign_api(data,self.access_token)
            if res == 401:
                refresh_res = self.handel_refresh_token()
                if refresh_res:
                    res = self.call_campaign_api(data,self.access_token)
            if type(res) == str:
                return JsonResponse({'status':'error','msg':res,'res':{}})
            return JsonResponse({'status':'success','msg':'','res':res['response']})
        if request.method == 'POST' and request.POST.get('file_id'):
            self.access_token,self.refresh_token = get_cookies(request)
            if not self.access_token: 
                return HttpResponseRedirect('/auth/login')
            file_id = request.POST.get('file_id')
            file_type = request.POST.get('file_type')
            data = {
                'file_type':file_type
            }
            res=self.call_delete_file_api(data,self.access_token,file_id)
            if res==401:
                refresh_res = self.handel_refresh_token()
                if refresh_res:
                    res = self.call_delete_file_api(data,self.access_token,file_id)
            if type(res)==str:
                return JsonResponse({'status':'error','msg':res,'res':{}})
            return JsonResponse({'status':'success','msg':'','res':res['response']})
        
        if request.method == 'POST' and request.POST.get('details',None):
            self.access_token,self.refresh_token = get_cookies(request)
            if not self.access_token:
                return HttpResponseRedirect('/auth/login')
            files = None
            if request.FILES:
                file=request.FILES.getlist('attachment')[0]
                files = [
                ('attachment', (file.name, file.read(), file.content_type))
            
            ]
            data ={
                'details':request.POST['details']
            }
            res = self.call_sendmsg_api(data,self.access_token,files)
            if res == 401:
                refresh_res = self.handel_refresh_token()
                if refresh_res:
                    res = self.call_sendmsg_api(data,self.access_token,files)
            return JsonResponse(res)
        
        return super().dispatch(request, *args, **kwargs)
      
    def updatejob_call_api(self, data, access_token):
        job_id = self.kwargs['pk']
        access_token = f"Bearer {access_token}"
        base_url = os.environ.get('BASE_URL') + f'jobs/updatejobdetails/{job_id}/'
        payload = json.dumps(data)
        res = makeJobPutCall(base_url, payload, access_token)
        status_code = res.status_code
        
        if status_code == 500:
            return "Oops, something went wrong"
        elif status_code == 401:
            return 401
        elif status_code == 200:
            try:
                response_data = json.loads(res.text)
                return response_data
            except json.JSONDecodeError:
                return "Error: Failed to parse response JSON"
        else:
            return ""
        
    def update_jobitem_call(self,data,access_token):
        access_token = f"Bearer {access_token}"
        base_url = os.environ.get('BASE_URL') + f'jobs/updatejobitem/'
        payload = json.dumps(data)
        res = makeJobPutCall(base_url, payload, access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops, something went wrong"
        elif status_code == 401:
            return 401
        elif status_code == 200:
            try:
                response_data = json.loads(res.text)
                return response_data
            except json.JSONDecodeError:
                return "Error: Failed to parse response JSON"
        else:
            return ""
        
    def upload_files(self,item_id,submitted_files,completed_files,eps_files=None,logo_files=None):
        access_token = f"Bearer {self.access_token}"
        base_url = env('BASE_URL')+'jobs/uploadfile/'
        if submitted_files:
            payload = {"file_type": "1","item_id": item_id}
            files = [
                ('file', (file.name, file.read(), file.content_type))
                for file in submitted_files
            ]
            res = makePutCall(base_url,payload,files,access_token)
        if completed_files:
            payload = {"file_type": "2","item_id": item_id}
            files = [
                ('file', (file.name, file.read(), file.content_type))
                for file in completed_files
            ]
            res = makePutCall(base_url,payload,files,access_token)
        if eps_files:
            files = [
                ('file', (file.name, file.read(), file.content_type))
                for file in eps_files
            ]
            payload = {"file_type": "4","item_id": item_id}
            res = makePutCall(base_url,payload,files,access_token)
        if logo_files:
            files = [
                ('file', (file.name, file.read(), file.content_type))
                for file in logo_files
            ]
            payload = {"file_type": "3","item_id": item_id}
            res = makePutCall(base_url,payload,files,access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops something went wrong"
        elif status_code == 401:
            return 401
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return ""


    def handel_refresh_token(self):
        payload = {
                    "refresh":self.refresh_token
                }
        api_res = account_service.call_refresh_api(payload)
        if type(api_res) == dict:
            token = api_res['response']
            self.access_token = token['access_token']
            self.refresh_token = token['refresh_token']
            self.is_set = True
            return True
        return False
    
        # campaign update
    def call_campaign_api(self,data,access_token):
        access_token = f"Bearer {access_token}"
        base_url=env('BASE_URL') + 'jobs/createcampaign/'
        payload = data
        res = campaign_post_api(base_url,payload,access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops! something went wrong"

        elif status_code == 401:
            return 401
                
        elif status_code != 200:
            msg = json.loads(res.text)
            return msg['msg']
        
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return ""
    
    def call_sendmsg_api(self,data,access_token,file):
        access_token = f"Bearer {access_token}"
        base_url=env('BASE_URL') + 'jobs/{}/sendmessages/'.format(self.id)
        res = sendmsg_post_call(base_url,data,file,access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops! something went wrong"

        elif status_code == 401:
            return 401
                
        elif status_code != 200:
            msg = json.loads(res.text)
            return msg['msg']
        
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return ""
    
    def call_getmsg_api(self,access_token,id):
        access_token = f"Bearer {access_token}"
        base_url=env('BASE_URL') + 'jobs/getjoblog/{}/'.format(id)
        res = makeGetCall(base_url,{},access_token)
        status_code = res.status_code
        if status_code == 500:
            return "Oops! something went wrong"

        elif status_code == 401:
            return 401
                
        elif status_code != 200:
            msg = json.loads(res.text)
            return msg['msg']
        
        elif status_code == 200:
            data = json.loads(res.text)
            return data
        return ""
    

    
    def form_valid(self,form,jobitem_form):
        job_obj = self.get_object()
        current_status = job_obj.status
        try:
            quote_no = form.cleaned_data['quote_no']
            user_email = form.cleaned_data['user_email']
            logo_name = form.cleaned_data['logo_name']
            logo_same_for_all = form.cleaned_data['logo_same_for_all']
            logo_same_for_all = True if logo_same_for_all == 'True' else False
            send_art_to_customer = form.cleaned_data['send_art_to_customer']
            send_art_to_customer = True if send_art_to_customer == 'True' else False
            proof_request_type = form.cleaned_data['proof_request_type']
            customer_no = form.cleaned_data['customer_no']
            customer_email = form.cleaned_data['customer_email']
            customer_name = form.cleaned_data['customer_name']
            segment_no = form.cleaned_data['segment_no']
            campaign = form.cleaned_data['campaign'].id if form.cleaned_data['campaign'] else None
            rep_no = form.cleaned_data['rep_no']
            status = form.cleaned_data['status']
            note = form.cleaned_data['note']
            jobitem_form = jobitem_form.cleaned_data
            job_data={
                "job_id": self.kwargs['pk'],
                "quote_no": quote_no,
                "user_email": user_email,
                "logo_name":logo_name ,
                "logo_same_for_all":logo_same_for_all ,
                "send_art_to_customer":send_art_to_customer ,
                "proof_request_type": proof_request_type,
                "campaign":campaign,
                "customer_no":customer_no,
                "customer_email":customer_email,
                "customer_name": customer_name,
                "segment_no":segment_no ,
                "note":note ,
                "status":status  
            }
            res = self.updatejob_call_api(job_data,self.access_token)
            if res == 401:
                refresh_res = self.handel_refresh_token()
                if refresh_res:
                    res = self.updatejob_call_api(job_data,self.access_token)
            item_data = [
                {
                    'id':item['id'].id if item['id'] else None,
                    'job_id_id':item['job_id'].id,
                    'item':item['item'],
                    'product_color':item['product_color'],
                    'imprint_color':item['imprint_color'],
                    'imprint_location':item['imprint_location'],
                    'imprint_method':item['imprint_method'],
                    'imprint_instructions':item['imprint_instructions'],
                    'submitted_files':item['submitted_files'],
                    'completed_files':item['completed_files'],
                    'eps_files':item['eps_files'],
                    'logo_files':item['logo_files']
                } for item in jobitem_form
            ]
            
            for item in item_data:
                submitted_files = item.pop('submitted_files')
                completed_files = item.pop('completed_files')
                eps_files = item.pop('eps_files')
                logo_files = item.pop('logo_files')
                res = self.update_jobitem_call(item,self.access_token)
                if res == 401:
                    refresh_res = self.handel_refresh_token()
                    if refresh_res:
                        res = self.update_jobitem_call(item,self.access_token)
                item_id = res['response']['id']
                if submitted_files or completed_files or eps_files or logo_files:
                    res = self.upload_files(item_id,submitted_files,completed_files,eps_files,logo_files)
                    if res == 401:
                        refresh_res = self.handel_refresh_token()
                        if refresh_res:
                            res = self.upload_files(item_id,submitted_files,completed_files,eps_files,logo_files)
            if current_status != status:
                if status == "4":  
                    data={
                        'subject':IN_QUERY_SUBJECT.format(job_obj.id,quote_no),
                        'body':IN_QUERY_BODY.format(quote_no, env('CLIENT_NAME')),
                        'to_email':job_obj.user.email,
                        'cc':env('EMAIL_CC').split(',')
                    }
                    send_email(data)
                elif status == "5":
                    data={
                        'subject':NEED_CORRECTION_SUBJECT.format(job_obj.id,quote_no),
                        'body':NEED_CORRECTION_BODY.format(quote_no,env('CLIENT_NAME')),
                        'to_email':job_obj.user.email,
                        'cc':env('EMAIL_CC').split(',')
                    }
                    send_email(data)
                elif status == "7":
                    link_file = create_file_link(job_obj.id)
                    job_id = job_obj.id
                    subject = JOB_COMPLETED_SUBJECT.format(env('CLIENT_NAME'),job_id, quote_no)
                    from_email = os.environ.get('EMAIL_USER')
                    to_email = job_obj.user.email
                    cc=env('EMAIL_CC').split(',')
                    client_name =env('CLIENT_NAME')
                    html_content = render_to_string('mail/send_mail_resp_com.html', context={'files': link_file,'quote_no': quote_no,'client_name':client_name})
                    # error_msg = None
                    send_background_email(job_id, subject, html_content, from_email, to_email, cc)
                    # try:
                    #     error_msg = send_background_email(job_id, subject, html_content, from_email, to_email, cc)
                    #     if error_msg is None:
                    #         return JsonResponse({'msg': 'Proof has been sent successfully.'})
                    # except:
                    #     return JsonResponse({'msg':'Please check your email credentials'})
                    # return JsonResponse({'msg':'Please check your email credentials'})

                elif status == "9":
                    data={
                        'subject':QUERIES_RESOLVED_SUBJECT.format(job_obj.id,quote_no),
                        'body':QUERIES_RESOLVED_BODY.format(quote_no,env('CLIENT_NAME')),
                        'to_email':job_obj.user.email,
                        'cc':env('EMAIL_CC').split(',')
                    }
                    send_email(data)
                elif status == "10":
                    data={
                        'subject':CUSTOMER_APPROVED_SUBJECT.format(job_obj.id,quote_no),
                        'body':CUSTOMER_APPROVED_BODY.format(quote_no,env('CLIENT_NAME')),
                        'to_email':job_obj.user.email,
                        'cc':env('EMAIL_CC').split(',')
                    }
                    send_email(data)
            messages.success(self.request, 'Job has been updated successfully.', extra_tags='job_msg')
            return HttpResponseRedirect(reverse_lazy('job:jobdetail',kwargs={'pk': self.kwargs['pk']}))
        except Exception as e:
            print(e)

    def get_context_data(self,*args,**kwargs):
        ctx = super(UpdateJobView,self).get_context_data(**kwargs)
        obj = self.get_object()
        if self.request.POST:
            ctx['jobitem_form'] = JobUpdateItemFormSet(self.request.POST, instance=obj)
            ctx['jobitem_form'].full_clean()
            form = self.form_class(self.request.POST, instance=obj)
            ctx['form'] = form
        else:
            ctx['jobitem_form'] = JobUpdateItemFormSet(instance=obj)
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            form.instance.submitted_date = form.instance.submitted_date.strftime('%m/%d/%Y %I:%M %p')
            ctx['form'] = form

        ctx['job_data'] = {
            'email' : obj.user.email,
            'submitted_date' : obj.submitted_date.strftime('%m/%d/%Y %I:%M %p'),
            'rep_no' : obj.rep_no
        }
        ctx['user'] = self.get_user(self.request)
        messages = self.call_getmsg_api(self.access_token,self.id)
        if messages == 401:
            payload = {
                "refresh":self.refresh_token
            }
            api_res = account_service.call_refresh_api(payload)
            if type(api_res) == dict:
                token = api_res['response']
                self.access_token = token['access_token']
                self.refresh_token = token['refresh_token']
                messages = self.call_getmsg_api(self.access_token,self.id)
                self.is_set = True
        messages = [] if type(messages) == str else messages['response']
        ctx['msgs'] = messages
        return ctx

def download_file(request,file_type=None,file_id=None,id=None):
    links = {}
    bucket_name = settings.LINODE_BUCKET
    client: boto3.s3 = boto3.client('s3',
    endpoint_url=settings.AWS_MAIN_S3_ENDPOINT_URL,
    aws_access_key_id=settings.LINODE_BUCKET_ACCESS_KEY,
    aws_secret_access_key=settings.LINODE_BUCKET_SECRET_KEY,
    config=boto3.session.Config(signature_version='s3v4')
    
    )
    if id:
        comp_files = CompletedFiles.objects.filter(jobitem__job_id__id=id, is_active=True).values_list('comp_files', flat=True)
        try:
            for comp_file in comp_files:
                file_name = comp_file.split('/')[-1]
                client.get_object(Bucket = bucket_name,Key = comp_file)
                download_url = client.generate_presigned_url('get_object',Params={'Bucket': bucket_name, 'Key': comp_file},ExpiresIn=600)
                links[file_name] = download_url
            return links
        except Exception as e:
            print(e)
            return None
    else:
        if file_type == 1:
            file = SubmittedFiles.objects.filter(id=file_id).first()
            file_key = file.sub_files
        if file_type == 2:
            file = CompletedFiles.objects.filter(id = file_id).first()
            file_key = file.comp_files
        if file_type == 4:
            file = EpsFiles.objects.filter(id = file_id).first()
            file_key = file.eps_files
        if file_type == 3:
            file = LogoFiles.objects.filter(id=file_id).first()
            file_key = file.logo_files
        if file_type == 5:
            file = JobLog.objects.filter(id=file_id).first()
            file_key = file.attachment
        try:
            client.get_object(Bucket=bucket_name,Key=file_key)
            download_url = client.generate_presigned_url('get_object',Params={'Bucket': bucket_name, 'Key': file_key},ExpiresIn=600)
            data = {
                'status': "success",
                'msg':download_url
            }
            return JsonResponse(data)
        except Exception as e:
            data = {
                'status': "error",
                'msg':"file not found"
            }
            return JsonResponse(data)



def download_comp_zip(request, id):
    comp_files = CompletedFiles.objects.filter(jobitem__job_id__id=id, is_active=True).values_list('comp_files', flat=True)
    bucket_name = settings.LINODE_BUCKET
    client = boto3.client(
        's3',
        endpoint_url=settings.AWS_MAIN_S3_ENDPOINT_URL,
        aws_access_key_id=settings.LINODE_BUCKET_ACCESS_KEY,
        aws_secret_access_key=settings.LINODE_BUCKET_SECRET_KEY,
    )
    zip_buffer = io.BytesIO()
    compression = zipfile.ZIP_DEFLATED 
    with contextlib.closing(zipfile.ZipFile(zip_buffer, 'w' , compression=compression)) as zip_file:
        for comp_file in comp_files:
            file_name = comp_file.split('/')[-1]
            
            with contextlib.closing(client.get_object(Bucket=bucket_name, Key=comp_file)['Body']) as s3_body:
                file_data = s3_body.read()
                zip_file.writestr(file_name, file_data)

    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="comp_files.zip"'
    zip_buffer.seek(0)
    response.write(zip_buffer.getvalue())
    return response


def create_file_link(id):
    queryset = CompletedFiles.objects.filter(jobitem__job_id__id=id, is_active=True)
    bucket_name = settings.LINODE_BUCKET
    client = boto3.client(
        's3',
        endpoint_url=settings.AWS_MAIN_S3_ENDPOINT_URL,
        aws_access_key_id=settings.LINODE_BUCKET_ACCESS_KEY,
        aws_secret_access_key=settings.LINODE_BUCKET_SECRET_KEY,
        config=boto3.session.Config(signature_version='s3v4')
    )
    file_links = {}

    for completed_file in queryset:
        key = completed_file.comp_files
        comp_file =key.split('/')[-1]
        response = client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': key},
            ExpiresIn=604800
        )
        file_links[comp_file]=response

    return file_links

def send_background_email(job_id, subject, html_content, from_email, to_email, cc):
    """
    Sends an email in the background.
    """
    try:
        email_message = EmailMultiAlternatives(
            subject=subject,
            body=html_content,
            from_email=from_email,
            to=[to_email],
            
            cc=cc
        )
        email_message.content_subtype = 'html'
        email_message.send()
        return None
    except smtplib.SMTPException as e:
        return HttpResponse(f"Email sending failed: {str(e)}")
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")
    
def send_email_customer(request):
    """
    Sends an email to a customer or responsible person based on request data.
    """
    cust_email = request.POST.get('customer_email')
    job_id = request.POST.get('id')
    quote_no = request.POST.get('quote_no')
    resp_email = request.POST.get('resp_email')
    subject = JOB_COMPLETED_SUBJECT.format(env('CLIENT_NAME'), job_id, quote_no)
    from_email = os.environ.get('EMAIL_USER')
    client_name = env('CLIENT_NAME')
    link_file = create_file_link(job_id)

    if cust_email:
        to_email = cust_email
    else:
        to_email = resp_email

    html_content = render_to_string('mail/send_mail_resp_com.html', context={'files': link_file, 'quote_no': quote_no, 'client_name': client_name})

    cc = env('EMAIL_CC').split(',')
    error_message = None
    try:
        error_message = send_background_email(job_id, subject, html_content, from_email, to_email, cc)
        if error_message is None:
            return JsonResponse({'msg': 'Proof has been sent successfully.'})
    except:
        return JsonResponse({'msg':'Please check your email credentials'})
    return JsonResponse({'msg':'Please check your email credentials'})
