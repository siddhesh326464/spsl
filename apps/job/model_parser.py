from api.job.serializers import JobLogSerializer,ViewJobSerializer,SendMessagesSerializer,ViewJobdetailSerializer,ViewJobItemListserializer,ViewNewjobitemserializer,ViewNewJobdetailSerializer,ViewCampaignSerializer,ViewSubmittedFiles,ViewCompletedFiles,ViewEpsFiles,ViewLogoFiles
def extract_job_list_to_dict(queryset):
    if queryset:
        serializer = ViewJobSerializer(queryset,many=True)
        return serializer.data
    return []

def extract_job_dict(queryset):
    if queryset:
        serializer = ViewJobdetailSerializer(queryset)
        return serializer.data
    return []

def job_details(queryset):
    if queryset:
        serializer=ViewJobdetailSerializer(queryset)
        return serializer.data
def extract_job_log_to_dict(queryset):
    if queryset:
        serializer=JobLogSerializer(queryset,many=True)
        return serializer.data
    return []

def extract_chat(queryset):
    if queryset:
        serializer=JobLogSerializer(queryset,many=True)
        return serializer.data
    else:
        return []
    
def create_entry(queryset):
    if queryset:
        serializer=JobLogSerializer(queryset=True,Many=True)
        return serializer.data
    else:
        return []

def alljob(queryset):
    if queryset:
        serializer=ViewJobSerializer(queryset,many=True)
        return serializer.data
    else:
        return[]
    
def msg_details(queryset):
    if queryset:
        serializer=JobLogSerializer(queryset)

        return(serializer.data)

def extract_job_item(queryset):
    if queryset:
        serializer = ViewJobItemListserializer(queryset)
        return (serializer.data)
    
def extract_new_job_item(queryset):
    if queryset:
        serializer = ViewNewjobitemserializer(queryset)
        return serializer.data
    
def new_job_details(queryset):
    if queryset:
        serializer=ViewNewJobdetailSerializer(queryset)
        return serializer.data
    

def extract_update_campaign(queryset):
    if queryset:
        serializer = ViewCampaignSerializer(queryset)
        return serializer.data
    else:
        []

def Extract_files(file_type,queryset):
    if file_type == 1:
        if queryset:
            serializer = ViewSubmittedFiles(queryset)
            return serializer.data
        
    if file_type == 2:
        if queryset:
            serializer = ViewCompletedFiles(queryset)
            return serializer.data
        
    if file_type == 3:
        if queryset:
            serializer = ViewLogoFiles(queryset)
            return serializer.data
        
    if file_type == 4:
        if queryset:
            serializer= ViewEpsFiles(queryset)
            return serializer.data