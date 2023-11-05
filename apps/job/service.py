from datetime import datetime
from api.job.serializers import JobLogSerializer
from apps.job.models import Job,Jobitem,Account
from django.core.paginator import EmptyPage, Paginator
from .models import Job,JobLog,SubmittedFiles,CompletedFiles,LogoFiles,EpsFiles,Campaign
from .model_parser import extract_job_list_to_dict,job_details,extract_job_dict,msg_details,alljob,extract_chat,extract_new_job_item,new_job_details,extract_update_campaign,Extract_files
from utils.notify import upload_Files,send_email,delete_file
from api.email_templates import *
from utils.constant import *
from apps.job.validation import *
from django.conf import settings
from django.db.models import Q
from utils.constant import JOB_STATUS
import datetime
def create_job(user,
               quote_no,
               logo_name,
               logo_same_for_all,
               send_art_to_customer,
               proof_request_type,
               campaign,
               customer_no,
               customer_email,
               customer_name,
               segment_no,
               note,
               status,
               items):
    obj = Campaign.objects.filter(id=campaign).last() if campaign else None
    data = {
        'user': user,
        'quote_no': quote_no,
        'logo_name': logo_name,
        'logo_same_for_all': logo_same_for_all,
        'send_art_to_customer': send_art_to_customer,
        'proof_request_type': proof_request_type,
        'campaign': obj,
        'customer_no': customer_no,
        'customer_email':customer_email,
        'customer_name': customer_name,
        'segment_no': segment_no,
        'rep_no': f"{user.first_name} {user.last_name} - {user.rep_no}",
        'note': note,
        'status': status,
        'created_by' : user,
        'updated_by':user #TODO:remove this field
    }
    validation_error=create_job_validation(user,status,proof_request_type)
    if validation_error:
        return validation_error 
    job=Job.objects.create(**data)
    if not job:
        return 2001
    item_data=[Jobitem(**dict(item,**{"job_id":job,"created_by":user})) for item in items]
    jobitem=Jobitem.objects.bulk_create(item_data)
    data={
        'subject':NEW_JOB_SUBJECT.format(job.id,job.quote_no),
        'body':NEW_JOB_BODY.format(job.id,env('CLIENT_NAME')),
        'to_email':job.user.email,
        'cc':env('EMAIL_CC').split(',')
    }
    send_email(data)
    return extract_job_dict(job)
    
def get_job_list(page, limit, status, user,all,logo,segment,requestnumber,quote,campaign,customerno,customername,repno):
    # queryset = Job.objects.filte r(status=str(status),user=user).order_by('-job_id')
    queryset = Job.objects.filter(status=str(status))
    if not queryset:
        return 2003
    if user.role == '1':
        queryset = queryset.filter(user=user)
    
    if all:
        campaign_ids = Campaign.objects.filter(name__icontains=all).values_list('id',flat=True)
        query = (Q(logo_name__icontains=all) | 
                Q(segment_no__icontains=all) |  
                Q(quote_no__icontains=all) |  
                Q(customer_no__icontains=all) | 
                Q(customer_name__icontains=all) | 
                Q(rep_no__icontains=all) |
                Q(campaign__id__in =campaign_ids))

        
        if all.isdigit():
            query = (query | Q(id=int(all)))

        queryset = queryset.filter(query)
    else:
        if logo:
            queryset = queryset.filter(logo_name__icontains=logo)

        if segment:
            queryset = queryset.filter(segment_no__icontains=segment)

        if requestnumber:
            if requestnumber.isdigit():
                queryset = queryset.filter(id=int(requestnumber))
            else:
                queryset = queryset.none()

        if quote:
            queryset = queryset.filter(quote_no__icontains=quote)

        if campaign:
            campaign_ids = Campaign.objects.filter(name__icontains=campaign).values_list('id',flat=True)
            queryset = queryset.filter(campaign__id__in=campaign_ids)

        if customerno:
            queryset = queryset.filter(customer_no__icontains=customerno)

        if customername:
            queryset = queryset.filter(customer_name__icontains=customername)

        if repno:
            queryset = queryset.filter(rep_no__icontains=repno)

    queryset = queryset.order_by('-id')
    if queryset:
        if limit is None:
            limit = queryset.count()
        if page is not None:
            paginator = Paginator(queryset, limit)
            try:
                queryset = paginator.page(page)
            except EmptyPage:
                queryset = []
        return extract_job_list_to_dict(queryset)
    return []

def get_job_details(job_id,user):
    queryset=Job.objects.filter(id=job_id).first()
    if not queryset:
        return 2001
    if user.role == '1':
        if queryset.user ==user:
            return job_details(queryset)
        else:
            return 2011     
    else:
        return job_details(queryset)       
    
def update_job_details(user,
                       job_id,
               quote_no,
               logo_name,
               logo_same_for_all,
               send_art_to_customer,
               proof_request_type,
               campaign,
               customer_no,
               customer_name,
               segment_no,
               note,
               status,
               items):
    queryset = Job.objects.filter(id=job_id)
    if not queryset:
        return 2001
    job_obj=queryset.first()
    if user.role == '1':
        if not queryset.filter(user=user):
            return 2010
    current_status=job_obj.status
    if status not in dict(Job.status.field.choices):
        return 2006
    if proof_request_type not in dict(PROOF_TYPE):
        return 2007    
    update_job = queryset.update(
            quote_no=quote_no,
            logo_name=logo_name,
            logo_same_for_all=logo_same_for_all,
            send_art_to_customer=send_art_to_customer,
            proof_request_type=proof_request_type,
            campaign=campaign,
            customer_no=customer_no,
            customer_name=customer_name,
            segment_no=segment_no,
            note=note,
            status=status,
            updated_by = user
        )
   
    for i in items:
        if 'id' in i:
            queryset1=Jobitem.objects.filter(id=i['id']).first()
            if queryset1:
                queryset1.item=i['item']
                queryset1.product_color=i['product_color']
                queryset1.imprint_color=i['imprint_color']
                queryset1.imprint_location=i['imprint_location']
                queryset1.imprint_method=i['imprint_method']
                queryset1.imprint_instructions=i['imprint_instructions']
                queryset1.updated_by=user
                queryset1.save()
        else:
            Jobitem.objects.create(job_id=queryset,**i)
    queryset = queryset.first()
    details=f"old status is {current_status} and new status is {status}"
    log_type = "put"
    log_data={
        'details':details,
        'log_type':log_type 
    }
    serializer = JobLogSerializer(data=log_data)
    if serializer.is_valid():
        serializer.save(job_id=job_obj,user_id=user)
    if current_status != status:
        if status == "4":  
            data={
                'subject':IN_QUERY_SUBJECT.format(job_id,quote_no),
                'body':IN_QUERY_BODY.format(env('CLIENT_NAME')),
                'to_email':queryset.user.email,
                'cc':env['EMAIL_CC']
            }
            send_email(data)
        elif status == "5":
            data={
                'subject':NEED_CORRECTION_SUBJECT.format(job_id,quote_no),
                'body':NEED_CORRECTION_BODY.format(quote_no),
                'to_email':queryset.user.email,
                'cc':env['EMAIL_CC']
            }
            send_email(data)
        elif status == "7":
            data={
                'subject':JOB_COMPLETED_SUBJECT.format(job_id,quote_no),
                'body':JOB_COMPLETED_BODY.format(quote_no,env),
                'to_email':queryset.user.email,
                'cc':env['EMAIL_CC']
            }
            send_email(data)
        elif status == "9":
            data={
                'subject':QUERIES_RESOLVED_SUBJECT.format(job_id,quote_no),
                'body':QUERIES_RESOLVED_BODY.format(quote_no),
                'to_email':queryset.user.email,
                'cc':env['EMAIL_CC']
            }
            send_email(data)
        elif status == "10":
            data={
                'subject':CUSTOMER_APPROVED_SUBJECT.format(job_id,quote_no),
                'body':CUSTOMER_APPROVED_BODY.format(quote_no),
                'to_email':queryset.user.email,
                'cc':['EMAIL_CC']
            }
            send_email(data)
    return extract_job_dict(queryset)
            

def send_messages(user,job_id,attachment,details):
    file_type='5'
    file_url = None
    if attachment:
        file_url = upload_Files(attachment,file_type,job_id)
    data={
        'attachment':file_url[0] if file_url else file_url,
        'details':details
    }
    queryset=Job.objects.filter(id=job_id).first()
    if not queryset:
        return 2001
    if user.role == '1':
        if not queryset.user == user:
            return 2012
    joblog=JobLog.objects.create(user_id_id=user.id,job_id=queryset,**data)
    data={
        'subject':CHAT_MESSAGE_SUBJECT.format(queryset.id,queryset.quote_no),
        # 'body':CHAT_MESSAGE_BODY.format(details,ATTACHMENT.format(attachment) if attachment else ""),
        'body':CHAT_MESSAGE_BODY.format(details,"",env('CLIENT_NAME')),
        'to_email':[queryset.user.email,user.email],
        'cc':['EMAIL_CC']
    }
    send_email(data)
    return msg_details(joblog)

def upload_image(user,file,file_type,item_id):
    job_id=Jobitem.objects.filter(id=item_id).first()
    if user.role == '1':
        if not job_id.job_id.user == user:
            return 2009
    validation_err=upload_image_validation(user,file_type)
    if validation_err:
        return validation_err
    file_url=upload_Files(file,file_type,job_id.job_id.id)
    print(file_url)
    obj=Jobitem.objects.filter(id=item_id).first()
    if not obj:
        return 2008
    if file_type=='1':
        for file in file_url:
            data={
                'sub_files':file,
                'jobitem':obj,
            }
            SubmittedFiles.objects.create(**data)
    elif file_type=='2':
        for file in file_url:
            data={
                'comp_files':file,
                'jobitem':obj,
            }
            CompletedFiles.objects.create(**data)
            job_id.completed_datetime = datetime.datetime.now()
            job_id.save()
    elif file_type=='3':
        for file in file_url:
            data={
                'logo_files':file,
                'jobitem':obj,
            }
            LogoFiles.objects.create(**data)
    elif file_type=='4':
        for file in file_url:
            data={
                'eps_files':file,
                'jobitem':obj,
            }
            EpsFiles.objects.create(**data)
    return file_url

def get_job_log(job_id):
    queryset=JobLog.objects.filter(job_id=job_id).order_by('-id')
    print(queryset)
    if queryset:
        return extract_chat(queryset)
    else:
        return []
    
def alldata(user,all,logo,segment,requestnumber,quote,campaign,customerno,customername,repno):
    queryset=Job.objects.all()
    if not queryset:
        return 2003
    if user.role == '1':
        queryset = queryset.filter(user=user)
    
    # if user.role == '3':
    #     queryset = queryset.filter(user=user)
    
    if all:
        campaign_ids = Campaign.objects.filter(name__icontains=all).values_list('id',flat=True)
        query = (Q(logo_name__icontains=all) | 
                Q(segment_no__icontains=all) |  
                Q(quote_no__icontains=all) |  
                Q(customer_no__icontains=all) | 
                Q(customer_name__icontains=all) | 
                Q(rep_no__icontains=all) |
                Q(campaign__id__in=campaign_ids)
                )
        
        if all.isdigit():
            query = (query | Q(id=int(all)))

        queryset = queryset.filter(query)
    else:
        if logo:
            queryset = queryset.filter(logo_name__icontains=logo)

        if segment:
            queryset = queryset.filter(segment_no__icontains=segment)

        if requestnumber:
            if requestnumber.isdigit():
                queryset = queryset.filter(id=int(requestnumber))
            else:
                queryset = queryset.none()

        if quote:
            queryset = queryset.filter(quote_no__icontains=quote)

        if campaign:
            campaign_ids = Campaign.objects.filter(name__icontains=campaign).values_list('id',flat=True)
            queryset = queryset.filter(campaign__id__in=campaign_ids)

        if customerno:
            queryset = queryset.filter(customer_no__icontains=customerno)

        if customername:
            queryset = queryset.filter(customer_name__icontains=customername)

        if repno:
            queryset = queryset.filter(rep_no__icontains=repno)
        
    new_queryset = queryset.filter(status=NEW).order_by('-id')
    new_count = new_queryset.count() 
    inprogress_queryset = queryset.filter(status=INPROGRESS).order_by('-id')
    inprogress_count = inprogress_queryset.count() 
    hold_queryset = queryset.filter(status=HOLD).order_by('-id')
    hold_count = hold_queryset.count() 
    query_queryset = queryset.filter(status=QUERY).order_by('-id')
    query_count = query_queryset.count() 
    correction_queryset = queryset.filter(status=CORRECTION).order_by('-id')
    correction_count = correction_queryset.count() 
    rush_correction_queryset = queryset.filter(status=RUSH_CORRECTION).order_by('-id')
    rush_correction_count = rush_correction_queryset.count() 
    completed_queryset = queryset.filter(status=COMPLETED).order_by('-id')
    completed_count = completed_queryset.count() 
    cancel_queryset = queryset.filter(status=CANCELED).order_by('-id')
    cancel_count = cancel_queryset.count() 
    query_resolve_queryset = queryset.filter(status=QUERY_RESOLVED).order_by('-id')
    query_resolve_count = query_resolve_queryset.count() 
    customer_approvel_queryset = queryset.filter(status=CUSTOMER_APPROVED).order_by('-id')
    customer_approvel_count = customer_approvel_queryset.count() 
    final_appoved_queryset = queryset.filter(status=FINAL_APPROVED).order_by('-id')
    final_appoved_count = final_appoved_queryset.count() 
    new_dict = alljob(new_queryset[:10])
    inprogress_dict = alljob(inprogress_queryset[:10])
    hold_dict = alljob(hold_queryset[:10])
    query_dict = alljob(query_queryset[:10])
    correction_dict = alljob(correction_queryset[:10])
    rush_correction_dict = alljob(rush_correction_queryset[:10])
    completed_dict = alljob(completed_queryset[:10])
    cancel_dict = alljob(cancel_queryset[:10])
    query_resolved_dict = alljob(query_resolve_queryset[:10])
    customer_approved_dict = alljob(customer_approvel_queryset[:10])
    final_appoved_dict = alljob(final_appoved_queryset[:10])    
    
    res = {
        "new" : new_dict,
        "in progress" : inprogress_dict,
        "on hold" : hold_dict, 
        "queries" : query_dict, 
        "corrections" : correction_dict, 
        "rush corrections" : rush_correction_dict, 
        "completed" : completed_dict, 
        "cancelled" : cancel_dict, 
        "queries resolved" : query_resolved_dict, 
        "customer approved" : customer_approved_dict, 
        "final approved" : final_appoved_dict,
        "total_count" : {
            'new' : new_count,
            'in progress' : inprogress_count,
            'on hold' : hold_count,
            'queries' : query_count,
            'corrections' : correction_count,
            'rush corrections' : rush_correction_count,
            'completed' : completed_count,
            'cancelled' : cancel_count,
            'queries resolved' : query_resolve_count,
            'customer approved' : customer_approvel_count,
            'final approved' : final_appoved_count,
        }
    }
    return res


def delete_jobitem(user,item_id):
    Files_to_delete = []
    queryset = Jobitem.objects.filter(id=item_id)
    if not queryset:
        return 2008
    if queryset.first().is_active == False:
        return 2015
    update_jobitem=queryset.update(is_active=False,
                                   updated_by = user
                                   )
    sub_files = SubmittedFiles.objects.filter(jobitem_id=item_id)
    for file in sub_files:
        if file.is_active == True:
            file.is_active = False
            file.save()
            Files_to_delete.append(file.sub_files)
    com_files = CompletedFiles.objects.filter(jobitem_id=item_id)
    for file in com_files:
        if file.is_active == True:
            file.is_active = False
            file.save()
            Files_to_delete.append(file.comp_files)
    logo_files = LogoFiles.objects.filter(jobitem_id=item_id)
    for file in logo_files:
        if file.is_active == True:
            file.is_active = False
            file.save()
            Files_to_delete.append(file.logo_files)
    eps_files = EpsFiles.objects.filter(jobitem_id=item_id)
    for file in eps_files:
        if file.is_active == True:
            file.is_active = False
            file.save()
            Files_to_delete.append(file.eps_files)
    if len(Files_to_delete) == 0 :
        return 2017
    del_file=delete_file(Files_to_delete)
    return []
    
    
def delete_single_file(user,file_id,file_type):
    if str(file_type) not in dict(FILE_TYPE):
        return 2005
    if str(file_type) == '1':
        sub_file_obj=SubmittedFiles.objects.filter(id=file_id)
        if sub_file_obj.first().is_active == False:
            return 2016
        obj = sub_file_obj.first()
        obj.is_active = False
        obj.save()
        del_sub_file=delete_file(sub_file_obj.first().sub_files)

    if str(file_type) =='2':
        com_file_obj=CompletedFiles.objects.filter(id=file_id)
        if com_file_obj.first().is_active == False:
            return 2016
        obj = com_file_obj.first()
        obj.is_active = False
        obj.save()
        del_com_file=delete_file(com_file_obj.first().comp_files)

    if str(file_type) == '3':
        logo_file_obj=LogoFiles.objects.filter(id=file_id)
        if logo_file_obj.first().is_active == False:
            return 2016
        obj =logo_file_obj.first()
        obj.is_active = False
        obj.save()
        del_sub_file=delete_file(logo_file_obj.first().logo_files)

    if str(file_type) == '4':
        eps_file_obj=EpsFiles.objects.filter(id=file_id)
        if eps_file_obj.first().is_active == False:
            return 2016
        obj = eps_file_obj.first()
        obj.is_active = False
        obj.save()
        del_eps_file=delete_file(eps_file_obj.first().eps_files)
    return Extract_files(file_type,obj)

def new_createjob(user,
               quote_no,
               logo_name,
               logo_same_for_all,
               send_art_to_customer,
               proof_request_type,
               campaign,
               customer_no,
               customer_email,
               customer_name,
               segment_no,
               note,
               status):
    obj = Campaign.objects.filter(id=campaign).last() if campaign else None
    data = {
        'user': user,
        'quote_no': quote_no,
        'logo_name': logo_name,
        'logo_same_for_all': logo_same_for_all,
        'send_art_to_customer': send_art_to_customer,
        'proof_request_type': proof_request_type,
        'campaign': obj,
        'customer_no': customer_no,
        'customer_email':customer_email,
        'customer_name': customer_name,
        'segment_no': segment_no,
        'rep_no': f"{user.first_name} {user.last_name} - {user.rep_no}",
        'note': note,
        'status': status,
        'created_by' : user,
        'updated_by':user #TODO:remove this field
    }
    validation_error=create_job_validation(user,status,proof_request_type)
    if validation_error:
        return validation_error 
    job=Job.objects.create(**data)
    return new_job_details(job)

def create_jobitem(user,
                   job_id,
                   item,
                   imprint_color,
                   product_color,
                   imprint_location, 
                   imprint_method,
                   imprint_instructions
                   ):
    data = {
        'job_id_id':job_id,
        'item':item,
        'imprint_color':imprint_color,
        'product_color':product_color,
        'imprint_location':imprint_location,
        'imprint_method':imprint_method,
        'imprint_instructions':imprint_instructions
    }
    jobitem = Jobitem.objects.create(**data)
    return extract_new_job_item(jobitem)
    
def new_update_job(user,
                job_id,
               quote_no,
               logo_name,
               logo_same_for_all,
               send_art_to_customer,
               proof_request_type,
               campaign,
               customer_no,
               customer_email,
               customer_name,
               segment_no,
               note,
               status):
    queryset = Job.objects.filter(id=job_id)
    if not queryset:
        return 2001
    job_obj=queryset.first()
    if user.role == '1':
        if not queryset.filter(user=user):
            return 2010
    current_status=job_obj.status
    if status not in dict(Job.status.field.choices):
        return 2006
    if proof_request_type not in dict(PROOF_TYPE):
        return 2007    
    update_job = queryset.update(
            quote_no=quote_no,
            logo_name=logo_name,
            logo_same_for_all=logo_same_for_all,
            send_art_to_customer=send_art_to_customer,
            proof_request_type=proof_request_type,
            campaign=campaign,
            customer_no=customer_no,
            customer_email=customer_email,
            customer_name=customer_name,
            segment_no=segment_no,
            note=note,
            status=status,
            updated_by = user
        )
    if current_status == status:
            return new_job_details(queryset)

    user =Account.objects.get(id=user.id)
    job = Job.objects.get(id=job_id)
    JobLog.objects.create(
        job_id=job,
        log_datetime=datetime.datetime.now(),
        user_id= user,
        prev_status =get_status_name(int(current_status)),
        new_status = get_status_name(int(status))
    )
    return new_job_details(queryset)
def get_status_name(status):
    for status_info in JOB_STATUS:
        if status_info['value'] == status:
            return status_info['name']
    return 'Unknown'  # Return a default value if the status is not found in the JOB_STATUS list

def update_jobitem(user,
                   id,
                   job_id,
                   item,
                   product_color,
                   imprint_color,
                   imprint_location,
                   imprint_method,
                   imprint_instructions
                   ):
    job_obj = Job.objects.filter(id=job_id).first()
    if id is not None:
        queryset = Jobitem.objects.filter(id=id)
        if not queryset:
            return 2001
        update_jobitem = queryset.update(
            item = item,
            product_color = product_color,
            imprint_color = imprint_color,
            imprint_location = imprint_location,
            imprint_method = imprint_method,
            imprint_instructions = imprint_instructions
        )
        res = queryset.last()
    else:
        data = {
            'item' : item,
            'product_color' : product_color,
            'imprint_color' : imprint_color,
            'imprint_location' : imprint_location,
            'imprint_method' : imprint_method,
            'imprint_instructions' : imprint_instructions
        }
        res = Jobitem.objects.create(job_id=job_obj,**data)
    return extract_new_job_item(res)


def create_campaign(user,id,name):
    if id !=None:
        campaign_exists =Campaign.objects.filter(name__exact=name).exists()
        if campaign_exists:
            return 2033 
        queryset = Campaign.objects.filter(id=id)
        if not queryset:
            return 2034
        camp=queryset.update(name=name,
                       updated_by = user
                       )
        obj=queryset.first()
    else:
        data={
            'name':name,
            'created_by':user
        }
        campaign_exists = Campaign.objects.filter(name__iexact=name).exists()
        if campaign_exists:
            return 2033 
        obj=Campaign.objects.create(**data)
    res=extract_update_campaign(obj)
    return res
