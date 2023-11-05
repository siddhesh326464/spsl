from django.template import Library
from utils.constant import FILE_TYPE

register = Library()

@register.filter
def job_status(dictionary, key):
    if not dictionary:
        return {}
    return dictionary.get(key.lower())

@register.filter
def job_status_count(dictionary, key):
    if not bool(dictionary):
        return 0
    data = dictionary.get(key.lower())
    return data

@register.filter
def get_files(job,item_id):
    sub_files_list = job.job.filter(id=item_id).filter(sub_files__id__isnull=False,sub_files__is_active=True).values('sub_files__sub_files','sub_files__id')
    sub_files=[dict(i,**{'file_name':i['sub_files__sub_files'].split('/')[-1],'file_type':FILE_TYPE[0][0]}) for i in list(sub_files_list)] 
    
    com_files_list = job.job.filter(id=item_id).filter(com_files__id__isnull=False,com_files__is_active = True).values('com_files__comp_files','com_files__id')
    com_files = [dict(i,**{'file_name':i['com_files__comp_files'].split('/')[-1],'file_type':FILE_TYPE[1][0]}) for i in list(com_files_list)] 

    logo_files_list = job.job.filter(id=item_id).filter(logo_files__id__isnull=False,logo_files__is_active=True).values('logo_files__logo_files','logo_files__id')
    logo_files = [dict(i,**{'file_name':i['logo_files__logo_files'].split('/')[-1],'file_type':FILE_TYPE[2][0]}) for i in list(logo_files_list)] 

    eps_files_list = job.job.filter(id=item_id).filter(eps_files__id__isnull=False,eps_files__is_active=True).values('eps_files__eps_files','eps_files__id')
    eps_files = [dict(i,**{'file_name':i['eps_files__eps_files'].split('/')[-1],'file_type':FILE_TYPE[3][0]}) for i in list(eps_files_list)] 

    
    return {'submitted_files':sub_files,'completed_files':com_files,'logo_files':logo_files,'eps_files':eps_files}

@register.filter
def get_date(datetime):
    datetime.split(" ")