from django.urls import path
from .views import JobView,CreateJobView,UpdateJobView,JobDetailview,download_file,download_comp_zip,download_file,send_email_customer

app_name = 'job'

urlpatterns = [
    path('',JobView.as_view(),name='home'),
    path('createjob/',CreateJobView.as_view(),name='createjob'),
    path('jobdetail/<int:pk>/',JobDetailview.as_view(),name='jobdetail'),
    path('updatejob/<int:pk>',UpdateJobView.as_view(),name='appupdatejob'),
    path('downloadfile/<int:file_type>/<int:file_id>',download_file,name='downloadfile'),
    path('download_zip_file/<int:id>',download_comp_zip,name='download_zip_file'),
    path('sendmailto_customer',send_email_customer,name = 'sendmailtocustomer'),

]