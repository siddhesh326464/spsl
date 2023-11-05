from django import forms
from .models import Job,Campaign,Jobitem,SubmittedFiles
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
# from django.forms.models import inlineformset_factory
from django.forms import modelformset_factory,inlineformset_factory
from django.forms.models import BaseModelFormSet
from multiupload.fields import MultiFileField,MultiUploadMetaInput
from django.conf import settings
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
env = os.getenv
class BaseJobItemFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseJobItemFormSet, self).__init__(*args, **kwargs)
        self.queryset = Jobitem.objects.none()

class CreateJobForm(forms.ModelForm):
    PROOF_TYPE_CHOICES =(
        ("0", "---------"),
        ('1','Standard Proof Request'),
        ('2','Apparel Proof Request'),
        ('3','Branded Guideline Request '),
        ('4','Complex Art Request'),
        ('5','Vectorization Logo Request')
    )
    STATUS_CHOICES =(
        ('1','New'),
        ('2','In Progress'),
        ('3','On Hold'),
        ('4','Queries'),
        ('5','Corrections'),
        ('6','Rush Corrections'),
        ('7','Completed'),
        ('8','Cancelled'),
        ('9','Queries Resolved'),
        ('10','Customer Approved'),
        ('11','Final Approved')
    )
    quote_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    user_email = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control form-control-sm'}))
    logo_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    logo_same_for_all = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    send_art_to_customer = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    proof_request_type = forms.ChoiceField(choices=PROOF_TYPE_CHOICES,widget=forms.Select(attrs={'class': 'form-select form-select-sm py-0'}))
    customer_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    customer_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm'}))
    customer_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    segment_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    campaign = forms.ModelChoiceField(label=_("Campaign"), queryset=Campaign.objects.all().order_by('name'),widget=forms.Select(attrs={'class':'form-select form-select-sm py-0'}))
    rep_no = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly','class': 'form-control form-control-sm'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES,widget=forms.Select(attrs={'disabled':True,'class': 'form-select form-select-sm py-0','style':'background: white;'}),initial="1")
    # status = forms.ChoiceField(choices=STATUS_CHOICES,initial=1,widget=forms.Textarea(attrs={'class': 'form-control form-control-sm', 'style': 'overflow: hidden;'}))
    note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-select-sm my-2','placeholder': 'Notes','rows':3,'cols':40}))
    item = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','data-id':'item_id'}))
    product_color = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    imprint_color = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    imprint_location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    imprint_method = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    imprint_instructions = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm','rows':1}))
    submitted_files = MultiFileField(min_num=1, 
                                     max_num=None, 
                                     max_file_size=None,
                                     widget=MultiUploadMetaInput(attrs={'class': 'form-control form-control-sm mb-1','multiple': 'multiple','onchange' : 'handleFileOnChange(this)'}))
    class Meta:
        model = Job
        exclude = ['updated_at','updated_by','created_by','submitted_date']

    # class Meta:
    #     model = Jobitem
    #     exclude = ('created_at','updated_at','job_id','updated_by','created_by','is_active','completed_datetime','id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['logo_name'].required = False
        self.fields['user_email'].required = False
        self.fields['logo_same_for_all'].required = False
        self.fields['send_art_to_customer'].required = False
        self.fields['segment_no'].required = False
        self.fields['campaign'].required = False
        self.fields['customer_email'].required = False
        self.fields['rep_no'].required = False
        self.fields['note'].required = False
        self.fields['status'].required = False
        self.fields['product_color'].required = False
        self.fields['imprint_color'].required = False
        self.fields['imprint_location'].required = False
        self.fields['imprint_method'].required = False
        self.fields['imprint_instructions'].required = False
        self.fields['submitted_files'].required = False

    def clean_proof_request_type(self):
        proof_request_type = self.cleaned_data['proof_request_type']
        if proof_request_type == '0':
            raise forms.ValidationError("Invalid choice.")

        return proof_request_type
    
    def clean_customer_email(self):
        send_art_to_customer = self.cleaned_data['send_art_to_customer']
        customer_email = self.cleaned_data['customer_email']
        if send_art_to_customer == 'True' and customer_email == "":
            return forms.ValidationError("customer email is required")
        return customer_email
    
    def clean_submitted_files(self):
        submitted_files = self.cleaned_data['submitted_files']
        l = [f.name.split('.')[-1] for f in submitted_files]
        # elements_not_in_list2 = [element for element in l if element not in ['pdf','png','ai','jpeg','jpg','PNG','zip','bmp','eps','rar','emb','7z','SIT','psd','cdr','indt','ppt','svg','tiff','xls','jpeg','docx','doc','bmp']]
        elements_not_in_list2 = [element for element in l if element not in env('FILES_EXTENSIONS')]
        print(elements_not_in_list2)
        if len(elements_not_in_list2) > 0:
            raise forms.ValidationError("please enter valid file type")
        return submitted_files
    
    def set_temp_files(self, files):
        self.temp_files = files

    def get_temp_files(self):
        return self.temp_files


class SubmittedFileForm(forms.ModelForm):
    sub_files = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control form-control-sm'}),required=True)

    class Meta:
        model = SubmittedFiles
        exclude = ('jobitem','is_active','created_at','updated_at')
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['sub_files'].required = True

#this is update job formview
class UpdateJobForm(forms.ModelForm):
    PROOF_TYPE_CHOICES =(
        ("0", "---------"),
        ('1','Standard Proof Request'),
        ('2','Apparel Proof Request'),
        ('3','Branded Guideline Request '),
        ('4','Complex Art Request'),
        ('5','Vectorization Logo Request')
    )
    STATUS_CHOICES =(

        ('1','New'),
        ('2','In Progress'),
        ('3','On Hold'),
        ('4','Queries'),
        ('5','Corrections'),
        ('6','Rush Corrections'),
        ('7','Completed'),
        ('8','Cancelled'),
        ('9','Queries Resolved'),
        ('10','Customer Approved'),
        ('11','Final Approved')
    )
    job_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','disabled':True}))
    quote_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    user_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','disabled':True}))
    logo_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    logo_same_for_all = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    send_art_to_customer = forms.CharField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    proof_request_type = forms.ChoiceField(choices=PROOF_TYPE_CHOICES,widget=forms.Select(attrs={'class': 'form-select form-select-sm py-0'}))
    customer_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    customer_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm'}))
    customer_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    submitted_date = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','disabled':True}))
    segment_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    campaign = forms.ModelChoiceField(label=_("Campaign"), queryset=Campaign.objects.all(),widget=forms.Select(attrs={'class':'form-select form-select-sm py-0'}))
    rep_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','disabled':True}))
    status = forms.ChoiceField(choices=STATUS_CHOICES,widget=forms.Select(attrs={'class': 'form-select form-select-sm py-0'}))
    note = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-select-sm my-2','placeholder': 'Note Regarding Job','rows':3,'cols':40}))
    class Meta:
        model = Job
        exclude = ['updated_at','updated_by','created_by']
    def __init__(self, *args, **kwargs):
        super(UpdateJobForm, self).__init__(*args, **kwargs)
        for choice in self.fields['status'].widget.choices:
            if choice[0] == '7':
                choice[2]['id'] = 'com_status'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['logo_name'].required = False
        self.fields['rep_no'].required = False
        self.fields['user_email'].required = False
        self.fields['logo_same_for_all'].required = False
        self.fields['send_art_to_customer'].required = False
        self.fields['segment_no'].required = False
        self.fields['campaign'].required = False
        self.fields['customer_email'].required = False
        self.fields['note'].required = False
        self.fields['job_id'].required = False
        self.fields['submitted_date'].required = False

    def clean_proof_request_type(self):
        proof_request_type = self.cleaned_data['proof_request_type']
        if proof_request_type == '0':
            raise forms.ValidationError("Invalid choice.")

        return proof_request_type
    
    def clean_customer_email(self):
        send_art_to_customer = self.cleaned_data['send_art_to_customer']
        customer_email = self.cleaned_data['customer_email']
        if send_art_to_customer == 'True' and customer_email == "":
            return forms.ValidationError("customer email is required")
        return customer_email
    
    
class UpdateJobItemForm(forms.ModelForm):
    id = forms.IntegerField(required=True)
    item = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','data-id':'item_id'}))
    product_color = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    imprint_color = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    imprint_location = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    imprint_method = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    completed_datetime = forms.CharField(widget=forms.TextInput(attrs={'disabled': True,'class': 'form-control form-control-sm','style': 'font-size: 13px;'}))
    # completed_datetime = forms.CharField(widget=forms.TextInput(attrs={'disabled': True, 'style': 'border: 0px; background-color: white; width:140px'}))

    imprint_instructions = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control form-control-sm','rows':1}))
    submitted_files = MultiFileField(min_num=1, 
                                     max_num=None, 
                                     max_file_size=None,
                                     widget=MultiUploadMetaInput(attrs={'class': 'form-control form-control-sm mb-1',  'multiple': 'multiple','onchange' : 'handleFileOnChange(this)','data-id':'submitted'})
                                     )
    completed_files = MultiFileField(min_num=1, 
                                     max_num=None, 
                                     max_file_size=None,
                                     widget=MultiUploadMetaInput(attrs={'class': 'form-control form-control-sm mb-1 ', 'multiple': 'multiple','onchange' : 'handleFileOnChange(this)', 'data-id':'completed'})
                                     )
    eps_files = MultiFileField(min_num=1, 
                                     max_num=None, 
                                     max_file_size=None,
                                     widget=MultiUploadMetaInput(attrs={'class': 'form-control form-control-sm mb-1', 'multiple': 'multiple','onchange' : 'handleFileOnChange(this)','data-id':'eps'})
                                     )
    logo_files = MultiFileField(min_num=1, 
                                     max_num=None, 
                                     max_file_size=None,
                                     widget=MultiUploadMetaInput(attrs={'class': 'form-control form-control-sm mb-1', 'multiple': 'multiple','onchange' : 'handleFileOnChange(this)','data-id':'logo'})
                                     )
    class Meta:
        model = Jobitem
        exclude = ('created_at','updated_at','updated_by','created_by','is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].required = True
        self.fields['product_color'].required = False
        self.fields['imprint_color'].required = False
        self.fields['imprint_method'].required = False
        self.fields['imprint_location'].required = False
        self.fields['imprint_instructions'].required = False
        self.fields['submitted_files'].required = False
        self.fields['eps_files'].required = False
        self.fields['logo_files'].required = False
        self.fields['completed_files'].required = False
        self.fields['completed_datetime'].required = False
        self.initial['completed_datetime'] = self.instance.completed_datetime.strftime('%d/%m/%Y %H:%M %p') if self.instance.completed_datetime else ""

    def clean_item(self):
        item = self.cleaned_data.get('item')
        if not item:
            raise forms.ValidationError('Please enter item')
        return item

    
JobUpdateItemFormSet = inlineformset_factory(
                                        Job,
                                        Jobitem,
                                       form=UpdateJobItemForm,
                                      can_delete=True,
                                    #   formset=BaseJobItemFormSet,
                                      can_delete_extra=False,
                                      validate_min=True,
                                      extra=0,
                                      min_num=1
                                      )

