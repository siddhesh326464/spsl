from utils.constant import PROOF_TYPE,FILE_TYPE
from apps.job.models import Job,Jobitem
from api import messages
def get_job_list_param_validation(page, limit):
    if page is not None:
        if len(str(page)) > 0:
            try:
                int(page)
            except:
                return 6015
        else:
            return 6017

    if limit is not None:
        if page is None:
            return 6019
        if len(str(limit)) > 0:
            try:
                int(limit)
            except:
                return 6016
        else:
            return 6018
    return ""

def upload_image_validation(user,file_type):
    
    if file_type not in dict(FILE_TYPE):
        return 2005
    # elif user.role == '1' and not file_type == '1':
    #     return 2009 
    return None  
    
def create_job_validation(user,status,proof_request_type):
    # if user.role=="3":
    #     return 2002
    # if status not in dict(Job.status.field.choices):
    #     return 2006
    if proof_request_type not in dict(PROOF_TYPE):
        return 2007
    return None

def update_job_validation():
    pass