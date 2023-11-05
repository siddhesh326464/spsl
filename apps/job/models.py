from django.db import models
from apps.account.models import Account
from api import messages
# Create your models here.

class Campaign(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    updated_by=models.ForeignKey(Account,on_delete=models.CASCADE, related_name='updated_by_campaign',null=True,blank=True)
    created_by=models.ForeignKey(Account,on_delete=models.CASCADE, related_name='created_by_campaign',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class Job(models.Model):
    class Meta:
        db_table = "job"
        verbose_name = "Jobs"
        verbose_name_plural = "Job"

    #TODO: need to capitilize string value
    PROOF_TYPE = [
        ('1','Standard Proof Request'),
        ('2','Apparel Proof Request'),
        ('3','Branded Guideline Request '),
        ('4','Complex Art Request'),
        ('5','Vectorization Logo Request')
    ]
    
    STATUS = [
        ('1','New'),
        ('2','In-Progress'),
        ('3','On Hold'),
        ('4','Queries'),
        ('5','Corrections'),
        ('6','Rush Corrections'),
        ('7','Completed'),
        ('8','Cancelled'),
        ('9','Queries Resolved'),
        ('10','Customer Approved'),
        ('11','Final Approved')
    ]
    user = models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,related_name='account')
    quote_no = models.CharField(max_length=100,null=True)
    logo_name = models.CharField(max_length=100,blank=True)
    logo_same_for_all = models.BooleanField(default=False,null=True)
    send_art_to_customer = models.BooleanField(null=True)
    submitted_date = models.DateTimeField(auto_now_add=True,null=True)
    proof_request_type = models.CharField(max_length=100,choices=PROOF_TYPE,default='Standard Proof Request')
    campaign = models.ForeignKey(Campaign,on_delete=models.CASCADE,blank=True,related_name='campaign',null=True)
    customer_no = models.CharField(max_length=100,blank=True)
    customer_email = models.EmailField(null=True,blank=True)
    customer_name = models.CharField(max_length=200,blank=True)
    segment_no = models.CharField(max_length=100,blank=True)
    rep_no = models.CharField(max_length=300,blank=True)
    note = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=100,choices=STATUS,default='New')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by=models.ForeignKey(Account,on_delete=models.CASCADE, related_name='updated_by_job_user')
    created_by=models.ForeignKey(Account,on_delete=models.CASCADE, related_name='created_by_job_user')

    def __str__(self):
        return str(self.id)
    
class Jobitem(models.Model):
    job_id=models.ForeignKey(Job,on_delete=models.CASCADE,related_name='job')
    item=models.CharField(max_length=100,blank=True)
    product_color=models.CharField(max_length=200,null=True)
    imprint_color=models.CharField(max_length=200,null=True)
    imprint_location=models.CharField(max_length=200,null=True)
    imprint_method=models.CharField(max_length=200,null=True,blank=True)
    imprint_instructions=models.CharField(max_length=500,null=True,blank=True)
    completed_datetime=models.DateTimeField(null=True,blank=True)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by=models.ForeignKey(Account,on_delete=models.CASCADE, related_name='updated_by_jobitem_user',null=True,blank=True)
    created_by=models.ForeignKey(Account,on_delete=models.CASCADE, related_name='created_by_jobitem_user',null=True,blank=True)

    class Meta:
        ordering = ('id',)
    
    def __str__(self):
       return str(self.id)


class SubmittedFiles(models.Model):
    jobitem=models.ForeignKey(Jobitem,on_delete=models.CASCADE,related_name="sub_files")
    sub_files=models.CharField(max_length=500,null=True)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    

class CompletedFiles(models.Model):
    jobitem=models.ForeignKey(Jobitem,on_delete=models.CASCADE,related_name="com_files")
    comp_files=models.CharField(max_length=500,null=True)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

class LogoFiles(models.Model):
    jobitem=models.ForeignKey(Jobitem,on_delete=models.CASCADE,related_name='logo_files')
    logo_files=models.CharField(max_length=500,null=True)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

class EpsFiles(models.Model):
    jobitem=models.ForeignKey(Jobitem,on_delete=models.CASCADE,related_name='eps_files')
    eps_files=models.CharField(max_length=500,null=True)
    is_active=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

class JobLog(models.Model):
    job_id=models.ForeignKey(Job,on_delete=models.CASCADE,related_name='job_log')
    log_datetime=models.DateTimeField(auto_now=True)
    user_id=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='job_log_user')
    attachment=models.CharField(max_length=500,blank=True,null=True)
    details=models.CharField(max_length=500)
    log_type=models.CharField(max_length=500,blank=True)
    prev_status = models.CharField(max_length=500,blank=True)
    new_status = models.CharField(max_length=500,blank=True)

    def __str__(self):
        return str(self.id)
    
