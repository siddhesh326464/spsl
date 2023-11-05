from django.urls import path
from api.job import views as api_job_view


urlpatterns = [
    path('addjob/', api_job_view.CreateJob.as_view(), name='addjob'),
    path('jobdetail/<int:job_id>/',api_job_view.JobDetails.as_view(),name='jobdetails'),
    path('alljob/<int:status>/', api_job_view.view_alljobs.as_view(), name='jobstatus'),
    path('alljobs/',api_job_view.AllJobs.as_view(),name='alljob'),
    path('updatejob/<int:job_id>/',api_job_view.JobUpdate.as_view(),name='updatejob'),
    path('<int:job_id>/sendmessages/',api_job_view.Send_messages.as_view(),name='sendmessages'),
    path('uploadfile/',api_job_view.UploadImage.as_view(),name='uploadimage'),
    path('getjoblog/<int:job_id>/',api_job_view.Job_log_All_Data.as_view()),
    path('deletejobitem/<int:item_id>/',api_job_view.DeleteJobitem.as_view(),name='deletejobitem'),
    path('deletefile/<int:file_id>/',api_job_view.Deletefile.as_view(),name='deletefile'),
    path('newcreatejob/',api_job_view.NewCreateJob.as_view(),name = 'Newcreatejob'),
    path('createjobitem/',api_job_view.CreateJobItem.as_view(),name = 'createjobitem'),
    path('updatejobdetails/<int:job_id>/',api_job_view.UpdateJob.as_view(),name = 'updatejobdetails' ),
    path('updatejobitem/',api_job_view.UpdateJobItem.as_view(),name = 'updatejobitem'),
    path('createcampaign/',api_job_view.AddCampaign.as_view(),name = 'createcampaign')
    #path('updatecampaign/<int:campaign_id>/',api_job_view.UpdateCampaign.as_view(),name = 'updatecampaign')
]