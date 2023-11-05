from rest_framework import serializers
from apps.job.models import Job,Jobitem,JobLog,Account,SubmittedFiles,CompletedFiles,LogoFiles,EpsFiles,Campaign
from utils.constant import PROOF_TYPE
from django.conf import settings
from django.db.models import Value,F
from django.db.models.functions import Concat
from utils.constant import FILE_TYPE
from django.conf import settings
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
env = os.getenv
class UploadSubmittedFileSerializer(serializers.Serializer):
    sub_files=serializers.FileField(required=True)

class CreateJobItemListSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    item=serializers.CharField(required=True, allow_blank=False, max_length=100)
    product_color=serializers.CharField(required=False, allow_blank=True,allow_null=True, max_length=100)
    imprint_color=serializers.CharField(required=False, allow_blank=True,allow_null=True, max_length=100)
    imprint_location=serializers.CharField(required=False, allow_blank=True,allow_null=True, max_length=100)
    imprint_method=serializers.CharField(required=False, allow_blank=True,allow_null=True, max_length=100)
    imprint_instructions=serializers.CharField(required=False, allow_blank=True,allow_null=True, max_length=500)
    job_id_id = serializers.IntegerField(required=False,allow_null=True)

class CreateJobSerializer(serializers.Serializer):
    quote_no=serializers.CharField(required=True, allow_blank=False, max_length=500)
    logo_name=serializers.CharField(required=False, allow_blank=True,allow_null=True, max_length=500)
    logo_same_for_all=serializers.BooleanField()
    send_art_to_customer=serializers.BooleanField()
    proof_request_type=serializers.CharField(required=True, allow_blank=False, max_length=500)
    campaign=serializers.IntegerField(allow_null=True,required = False)
    customer_no=serializers.CharField(required=True, allow_blank=False, max_length=500)
    customer_email = serializers.EmailField(allow_blank=True,required = False,allow_null=True)
    customer_name=serializers.CharField(required=True, allow_blank=False, max_length=500)
    segment_no=serializers.CharField(required=False,allow_blank=True,allow_null=True, max_length=500)
    note=serializers.CharField(required=False, allow_blank=True,allow_null=True, max_length=500)
    status=serializers.CharField(required=True, allow_blank=False, max_length=500)
    item = CreateJobItemListSerializer(many=True)

class UserSerialiser(serializers.Serializer):
    class Meta:
        Model=Account
        feilds='__all__'


class ViewJobItemListserializer(serializers.ModelSerializer):
    sub_files = serializers.SerializerMethodField()
    com_files = serializers.SerializerMethodField()
    logo_files = serializers.SerializerMethodField()
    eps_files = serializers.SerializerMethodField()
    completed_datetime = serializers.SerializerMethodField()
    class Meta:
        model=Jobitem
        fields=['id','item','product_color','imprint_color','imprint_location','imprint_instructions','imprint_method','sub_files','com_files','logo_files','eps_files','completed_datetime']

    def get_sub_files(self,instance):
        sub_file = instance.sub_files.filter(is_active = True).values('id','sub_files')
        sub_file = [dict(i,**{'file_name':i['sub_files'].split('/')[-1],'file_type':FILE_TYPE[0][0]}) for i in list(sub_file)]
        return sub_file
    
    def get_com_files(self,instance):
        com_file = instance.com_files.filter(is_active = True).values('id','comp_files','updated_at')
        com_file = [dict(i,**{'file_name':i['comp_files'].split('/')[-1],'file_type':FILE_TYPE[1][0]}) for i in list(com_file)]
        return com_file
    
    def get_logo_files(self,instance):
        logo_file = instance.logo_files.filter(is_active = True).values('id','logo_files')
        logo_file = [dict(i,**{'file_name':i['logo_files'].split('/')[-1],'file_type':FILE_TYPE[2][0]}) for i in list(logo_file)]
        return logo_file
    
    def get_eps_files(self,instance):
        eps_file = instance.eps_files.filter(is_active = True).values('id','eps_files')
        eps_file = [dict(i,**{'file_name':i['eps_files'].split('/')[-1],'file_type':FILE_TYPE[3][0]}) for i in list(eps_file)]
        return eps_file
    
    def get_completed_datetime(self,instance):
        format_completed_date = instance.completed_datetime.strftime('%d/%m/%Y %H:%M %p') if instance.completed_datetime else ""
        return format_completed_date

class ViewJobdetailSerializer(serializers.ModelSerializer):
    job=serializers.SerializerMethodField()
    submitted_date=serializers.SerializerMethodField()
    customer_email=serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    class Meta:
        model=Job
        fields=['id',
                'user',
                "quote_no",
                'logo_name',
                'logo_same_for_all',
                'submitted_date',
                'send_art_to_customer',
                'customer_name',
                'segment_no',
                'customer_no',
                'customer_email',
                'proof_request_type',
                'campaign',
                'rep_no',
                'note',
                'status',
                'job'
                ]

    def get_job(self,instance):
        jobItem = instance.job.filter(is_active=True)
        jobItemList = ViewJobItemListserializer(jobItem,many=True)
        return jobItemList.data
    
    def get_submitted_date(self,instance):
        return instance.submitted_date.strftime('%d/%m/%Y %H:%M %p')
    
    def get_customer_email(self,instance):
        customer_email = instance.customer_email if instance.customer_email else ""
        return customer_email
    def get_user(self,instance):
        return instance.user.email

class ViewJobSerializer(serializers.ModelSerializer):
    submitted_date = serializers.SerializerMethodField()
    proof_request_type = serializers.SerializerMethodField()
    campaign = serializers.SerializerMethodField()

    class Meta:
        model=Job
        fields=['id',"quote_no",'submitted_date','customer_name','customer_no','proof_request_type','logo_name','campaign','rep_no']
    
    def get_submitted_date(self,instance):
        return instance.submitted_date.strftime('%m-%d-%Y %H:%M %p')
    
    def get_campaign(self,instance):
        compaign = instance.campaign.name if instance.campaign else ""
        return compaign
    
    def get_proof_request_type(self,instance):
        value = [b for a,b in PROOF_TYPE if a==instance.proof_request_type][0]
        return value
    
class SendMessagesSerializer(serializers.Serializer):
    attachment=serializers.FileField(required=False,allow_null=True)
    details=serializers.CharField(max_length=200)


class JobLogSerializer(serializers.Serializer):
    details = serializers.CharField(max_length=200)
    log_type = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return JobLog.objects.create(**validated_data)
    
class UplaodFileSerializer(serializers.Serializer):
    file = serializers.ListField(child=serializers.FileField())
    item_id=serializers.IntegerField()
    # file = serializers.FileField()
    file_type = serializers.CharField(max_length=10)
    def validate_file(self,value):
        if type(value) == list:
            for v in value:
                file_extension = v.name.split('.')
        else:
            file_extension = value.name.split('.')
        # if file_extension[-1] not in ['pdf','png','ai','jpeg','jpg','PNG','eps','bmp','zip']:
        # if file_extension[-1] not in ['pdf','png','ai','jpeg','jpg','PNG','zip','bmp','eps','rar','emb','7z','SIT','psd','cdr','indt','ppt','svg','tiff','xls','jpeg','docx','doc','bmp']:
        if file_extension[-1] not in env('FILES_EXTENSIONS'):
            raise serializers.ValidationError("Invalid file type")   
        return value


class JobViewSerialiser(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields='__all__'

class JobLogSerializer(serializers.ModelSerializer):
    user_id =serializers.SerializerMethodField()
    log_datetime = serializers.SerializerMethodField()
    attachment = serializers.SerializerMethodField()
    filename = serializers.SerializerMethodField()
    class Meta:
        model=JobLog
        fields=['id','details','user_id','log_datetime','attachment','filename','prev_status','new_status']

    def get_user_id(self,instance):
        return "{} {}".format(instance.user_id.first_name,instance.user_id.last_name)
    
    def get_log_datetime(self,instance):
        return instance.log_datetime.strftime('%m-%d-%Y %H:%M %p')
    
    def get_attachment(self,instance):
        attachment = ({'file_name':instance.attachment.split('/')[-1],'file_type':FILE_TYPE[4][0]}) if instance.attachment else ""
        return attachment
        
    def get_filename(self,instance):
        file_name = instance.attachment.split('/')[-1] if instance.attachment else ""
        return file_name

class JobItemDeleteSerializer(serializers.Serializer):
    is_active=serializers.BooleanField()

class FileDeleteSerializer(serializers.Serializer):
    file_type = serializers.IntegerField()

class NewJobcrewateserializer(serializers.Serializer):
    quote_no=serializers.CharField(required=True, allow_blank=False, max_length=50)
    logo_name=serializers.CharField(required=False, allow_blank=True,allow_null=True, max_length=50)
    logo_same_for_all=serializers.BooleanField()
    send_art_to_customer=serializers.BooleanField()
    proof_request_type=serializers.CharField(required=True, allow_blank=False, max_length=50)
    campaign=serializers.IntegerField(allow_null=True,required = False)
    customer_no=serializers.CharField(required=True, allow_blank=False, max_length=50)
    customer_email = serializers.EmailField(allow_blank=True,required = False,allow_null=True)
    customer_name=serializers.CharField(required=True, allow_blank=False, max_length=50)
    segment_no=serializers.CharField(required=False,allow_blank=True,allow_null=True, max_length=50)
    note=serializers.CharField(required=False, allow_blank=True,allow_null=True, max_length=500)
    status=serializers.CharField(required=True, allow_blank=False, max_length=50)

class ViewNewjobitemserializer(serializers.ModelSerializer):
    class Meta:
        model=Jobitem
        fields=['id','item','product_color','imprint_color','imprint_location','imprint_method']


class ViewNewJobdetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Job
        fields=['id',"quote_no",'submitted_date','customer_name','customer_no','proof_request_type','logo_name','campaign','rep_no','status']

class CampaignSerializer(serializers.Serializer):
    id=serializers.IntegerField(required=False)
    name=serializers.CharField(required=True, allow_blank=False, allow_null=True, max_length=500)

class ViewCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model=Campaign
        fields=['id','name']

        
class ViewSendMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobLog
        fields = ['id','details','attachment']


class Downloadfileserializer(serializers.Serializer):
    file_type = serializers.IntegerField()


class ViewSubmittedFiles(serializers.ModelSerializer):
    class Meta:
        model = SubmittedFiles
        fields = ['id','sub_files']

class ViewCompletedFiles(serializers.ModelSerializer):
    class Meta:
        model = CompletedFiles
        fields = ['id','comp_files','updated_at']

class ViewEpsFiles(serializers.ModelSerializer):
    class Meta:
        model = EpsFiles
        fields = ['id','eps_files']

class ViewLogoFiles(serializers.ModelSerializer):
    class Meta:
        model = LogoFiles
        fields = ['id','logo_files']