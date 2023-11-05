from django.contrib import admin
from apps.job.models import Job,Jobitem,JobLog,SubmittedFiles,CompletedFiles,LogoFiles,EpsFiles,Campaign
# Register your models here.
class JobModelAdmin(admin.ModelAdmin):
    list_display=['user','quote_no','logo_name','logo_same_for_all','send_art_to_customer','submitted_date','proof_request_type','campaign','customer_no','customer_name','segment_no','rep_no','note','status']
    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.save()
    #         JobLog.objects.create(job_id=obj,user_id=request.user, details="Created an account",log_type='POST')
admin.site.register(Job,JobModelAdmin)      

class JobitemlistModelAdmin(admin.ModelAdmin):
    list_display=['id','job_id','item','product_color','imprint_color','imprint_location','imprint_method','imprint_instructions','completed_datetime']
admin.site.register(Jobitem,JobitemlistModelAdmin)

class JobItem_SubFilesModelAdmin(admin.ModelAdmin):
    list_display=['id','jobitem','sub_files']
admin.site.register(SubmittedFiles,JobItem_SubFilesModelAdmin)

class JobItem_CompFilesModelAdmin(admin.ModelAdmin):
    list_display=['id','jobitem','comp_files']
admin.site.register(CompletedFiles,JobItem_CompFilesModelAdmin)

class JobItem_LogoFilesModelAdmin(admin.ModelAdmin):
    list_display=['id','jobitem','logo_files']
admin.site.register(LogoFiles,JobItem_LogoFilesModelAdmin)

class JobItem_EpsFilesModelAdmin(admin.ModelAdmin):
    list_display=['id','jobitem','eps_files']
admin.site.register(EpsFiles,JobItem_EpsFilesModelAdmin)


class Job_LogModelAdmin(admin.ModelAdmin):
    list_display=['id','job_id','log_datetime','user_id','attachment','details','log_type']
admin.site.register(JobLog,Job_LogModelAdmin)

class JobCampaignAdmin(admin.ModelAdmin):
    list_display=['id','name']
admin.site.register(Campaign,JobCampaignAdmin)
# class Activity(admin.ModelAdmin):
#     list_display=['log_id','job_id','log_datetime','user_id','attachment','details','log_type']
# admin.site.register(Job_Log,Activity)


