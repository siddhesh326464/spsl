from django.shortcuts import render
# Create your views here.
from django.shortcuts import render
from rest_framework import generics,parsers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from utils.constant import *
from utils.common import extract_from_request,dispatch_response
from apps.job import service as job_service
from apps.job import validation as job_validate
from drf_yasg import openapi
from api.job.serializers import CreateJobSerializer,ViewJobSerializer,SendMessagesSerializer,UplaodFileSerializer,JobLogSerializer,ViewJobdetailSerializer,FileDeleteSerializer,JobItemDeleteSerializer,NewJobcrewateserializer,CreateJobItemListSerializer,CampaignSerializer,Downloadfileserializer
from drf_yasg.utils import swagger_auto_schema
from utils.constant import*
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from apps.job import service as job_servises
from api.job.validation import validate_rdata
from api import messages
class Job_log_All_Data(generics.ListAPIView):
    allowed_method=('GET',)
    permission_classes=[IsAuthenticated]
    serializer_class=JobLogSerializer
    @swagger_auto_schema(
        tags=[API_JOB]

    )
    def get(self,request,job_id):
        res=job_service.get_job_log(job_id)
        return dispatch_response(res)
    
       
class view_alljobs(generics.ListAPIView):
    """
    This function is used view all the job with respect to status
    if status is not with in it raise error
    """
    allowed_method = ("GET", )
    permission_classes = (IsAuthenticated, )
    serializer_class = ViewJobSerializer

    page = openapi.Parameter(
        'page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)

    limit = openapi.Parameter(
        'limit', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
    all = openapi.Parameter(
        'all', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    logo= openapi.Parameter(
        'logo', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    segment = openapi.Parameter(
        'segment', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    requestnumber = openapi.Parameter(
        'requestnumber', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    quote = openapi.Parameter(
        'quote', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    campaign = openapi.Parameter(
        'campaign', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    customerno = openapi.Parameter(
        'customerno', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    customername = openapi.Parameter(
        'customername', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    repno = openapi.Parameter(
        'repno', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    @swagger_auto_schema(
        manual_parameters=[page, limit,all,logo,segment,requestnumber,quote,campaign,customerno,customername,repno],
        tags=[API_JOB]

    )
    def get(self, request,status):
        page, limit,all,logo,segment,requestnumber,quote,campaign,customerno,customername,repno = extract_from_request(
            request, "page", "limit","all","logo","segment","requestnumber","quote","campaign","customerno","customername","repno")
        user = request.user
        validate_response = job_validate.get_job_list_param_validation(
            page, limit)
        

        if type(validate_response) == int:
            return dispatch_response(validate_response)
        res = job_service.get_job_list(page,limit,status,user,all,logo,segment,requestnumber,quote,campaign,customerno,customername,repno)
        return dispatch_response(res)
      
class CreateJob(generics.GenericAPIView):
    allowed_methods = ("POST",)
    serializer_class = CreateJobSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="\
            <b>Username: </b> <a style='text-decoration:none !important; color:black; pointer-events:none;'>admin@addnectar.com </a> <br><br> \
            <b>Pasword: </b> Add@2023",
        
        tags=[API_JOB]
    )
    def post(self,request):
        data=request.data
        serializer=CreateJobSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        validation_error=validate_rdata(data)
        if type(validation_error) != str:
            return dispatch_response(validation_error) 
        data= serializer.validated_data
        res=job_servises.create_job(request.user,
                                    data['quote_no'],
                                    data['logo_name'],
                                    data['logo_same_for_all'],
                                    data['send_art_to_customer'],
                                    data['proof_request_type'],
                                    data['campaign'],
                                    data['customer_no'],
                                    data['customer_email'],
                                    data['customer_name'],
                                    data['segment_no'],
                                    data['note'],
                                    data['status'],
                                    data['item']
                                )
        return dispatch_response(res)

class JobDetails(generics.GenericAPIView):
    allowed_methods = ("GET",)
    serializer_class = ViewJobdetailSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="\
            <b>Username: </b> <a style='text-decoration:none !important; color:black; pointer-events:none;'>admin@addnectar.com </a> <br><br> \
            <b>Pasword: </b> Add@2023",
        
        tags=[API_JOB]
    )
    def get(self,request,job_id):
        res=job_servises.get_job_details(job_id,request.user)
        return dispatch_response(res)

class JobUpdate(generics.UpdateAPIView):
    allowed_methods = ("PUT",)
    serializer_class = CreateJobSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="\
            <b>Username: </b> <a style='text-decoration:none !important; color:black; pointer-events:none;'>admin@addnectar.com </a> <br><br> \
            <b>Pasword: </b> Add@2023",
        
        tags=[API_JOB]
    )
    def put(self,request,job_id):
        data=request.data
        serializer=CreateJobSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        validation_error=validate_rdata(data)
        if type(validation_error) != str:
            return dispatch_response(validation_error)         
        data=serializer.validated_data
        res=job_servises.update_job_details(request.user,
                                            job_id,
                                    data['quote_no'],
                                    data['logo_name'],
                                    data['logo_same_for_all'],
                                    data['send_art_to_customer'],
                                    data['proof_request_type'],
                                    data['campaign'],
                                    data['customer_no'],
                                    data['customer_name'],
                                    data['segment_no'],
                                    data['note'],
                                    data['status'],
                                    data['item']
                                    )
        return dispatch_response(res)

class Send_messages(generics.GenericAPIView):
    allowed_methods = ("POST",)
    serializer_class = SendMessagesSerializer
    parser_classes = (parsers.MultiPartParser,parsers.FormParser) 
    def post(self,request,job_id):
        serializer=SendMessagesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        data=serializer.validated_data
        attachment = None
        if 'attachment' in data.keys():
            attachment = data['attachment']
        res=job_servises.send_messages(request.user,
                                       job_id,
                                       attachment,
                                       data['details']
                                       )
        return dispatch_response(res)
    
class AllJobs(generics.GenericAPIView):
    allowed_methods = ("GET",)
    serializer_class = ViewJobSerializer
    permission_classes = [IsAuthenticated]

    all = openapi.Parameter(
        'all', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    logo= openapi.Parameter(
        'logo', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    segment = openapi.Parameter(
        'segment', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    requestnumber = openapi.Parameter(
        'requestnumber', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    quote = openapi.Parameter(
        'quote', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    campaign = openapi.Parameter(
        'campaign', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    customerno = openapi.Parameter(
        'customerno', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    customername = openapi.Parameter(
        'customername', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    repno = openapi.Parameter(
        'repno', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=False)
    

    @swagger_auto_schema(
        manual_parameters=[all,logo,segment,requestnumber,quote,campaign,customerno,customername,repno],
        tags=[API_JOB]
    )
    def get(self, request):
        all,logo,segment,requestnumber,quote,campaign,customerno,customername,repno = extract_from_request(
            request, "all", "logo","segment","requestnumber","quote","campaign","customerno","customername","repno")
        user = request.user
        res = job_service.alldata(user,all,logo,segment,requestnumber,quote,campaign,customerno,customername,repno)
        return dispatch_response(res)
    
class UploadImage(generics.GenericAPIView):
    allowed_methods = ("PUT",)
    serializer_class = UplaodFileSerializer
    permission_classes = [IsAuthenticated]
    # parser_classes = (parsers.MultiPartParser,parsers.FormParser)

    @swagger_auto_schema(
        operation_description="\
            <b>file: </b> <a style='text-decoration:none !important; color:black; pointer-events:none;'>1011.png</a> <br><br> \
            <b>file_type: </b> 1",
        
        tags=[API_JOB]
    )
    def put(self,request):
        serializer=UplaodFileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        res = job_servises.upload_image(request.user,
                                        data['file'],
                                        data['file_type'],
                                        data['item_id']
                                        )
        
        return dispatch_response(res) 

class DeleteJobitem(generics.GenericAPIView):
    allowed_methods = ("PUT",)
    serializer_class = JobItemDeleteSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="\
            <b>file: </b> <a style='text-decoration:none !important; color:black; pointer-events:none;'>1011.png</a> <br><br> \
            <b>file_type: </b> 1",
        
        tags=[API_JOB]
    )
    def put(self,request,item_id):
        res = job_servises.delete_jobitem(request.user,
                                          item_id,
                                          )
        return dispatch_response(res)

class Deletefile(generics.GenericAPIView):
    allowed_methods = ("PUT",)
    serializer_class = FileDeleteSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="\
            <b>file: </b> <a style='text-decoration:none !important; color:black; pointer-events:none;'>1011.png</a> <br><br> \
            <b>file_type: </b> 1",
        
        tags=[API_JOB]
    )
    def put(self,request,file_id):
        serializer=FileDeleteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        res=job_servises.delete_single_file(request.user,
                                     file_id,
                                     data['file_type'],
                                     )
        return dispatch_response(res)
    
class NewCreateJob(generics.GenericAPIView):
    allowed_methods = ("POST",)
    serializer_class = NewJobcrewateserializer
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = NewJobcrewateserializer(data = request.data)
        if not serializer.is_valid():
            return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        data= serializer.validated_data
        res = job_servises.new_createjob(request.user,
                                    data['quote_no'],
                                    data['logo_name'],
                                    data['logo_same_for_all'],
                                    data['send_art_to_customer'],
                                    data['proof_request_type'],
                                    data['campaign'],
                                    data['customer_no'],
                                    data['customer_email'],
                                    data['customer_name'],
                                    data['segment_no'],
                                    data['note'],
                                    data['status'])
        return dispatch_response(res)
    
class CreateJobItem(generics.GenericAPIView):
    allowed_methods = ("POST",)
    serializer_class = CreateJobItemListSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request):
       
        serializer = CreateJobItemListSerializer( data =request.data)
        if not serializer.is_valid():
            return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        data= serializer.validated_data
        res = job_servises.create_jobitem(request.user,
                                          data['job_id_id'],
                                          data['item'],
                                          data['product_color'],
                                          data['imprint_color'],
                                          data['imprint_location'],
                                          data['imprint_method'],
                                          data['imprint_instructions']
                                          )
        return dispatch_response(res)
    
class UpdateJob(generics.GenericAPIView):
    allowed_methods = ("PUT",)
    serializer_class = NewJobcrewateserializer
    permission_classes = [IsAuthenticated]  

    def put(self,request,job_id):
        serializer = NewJobcrewateserializer(data = request.data)
        if not serializer.is_valid():
            return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        res = job_servises.new_update_job(request.user,
                                            job_id,
                                    data['quote_no'],
                                    data['logo_name'],
                                    data['logo_same_for_all'],
                                    data['send_art_to_customer'],
                                    data['proof_request_type'],
                                    data['campaign'],
                                    data['customer_no'],
                                    data['customer_email'],
                                    data['customer_name'],
                                    data['segment_no'],
                                    data['note'],
                                    data['status'])
        return dispatch_response(res)
    

class UpdateJobItem(generics.GenericAPIView):
    allowed_methods = ("PUT",)
    serializer_class = CreateJobItemListSerializer
    permission_classes = [IsAuthenticated] 
    def put(self,request):
        serializer = CreateJobItemListSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        res = job_servises.update_jobitem(request.user,
                                          data['id'],
                                          data['job_id_id'],
                                          data['item'],
                                          data['product_color'],
                                          data['imprint_color'],
                                          data['imprint_location'],
                                          data['imprint_method'],
                                          data['imprint_instructions'])
        return dispatch_response(res)


class AddCampaign(generics.GenericAPIView):
    allowed_methods = ('POST', )
    serializer_class = CampaignSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        id = data['id'] if 'id' in data.keys() else None
        res = job_servises.create_campaign(request.user,
                                           id,
                                           data['name']
                                           )
        return dispatch_response(res)
        

# class UpdateCampaign(generics.GenericAPIView):
#     allowed_methods = ('PUT',)
#     serializer_class = CampaignSerializer
#     permission_classes = [IsAuthenticated]

#     def put(self, request, campaign_id):
#         serializer = self.get_serializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         data = serializer.validated_data
#         res = job_servises.update_campaign(request.user,campaign_id, data['name'])
#         return dispatch_response(res)
