import os,boto3,datetime,threading
from boto3.s3.transfer import S3Transfer
from django.conf import settings
from django.core.files.storage import default_storage
from dotenv import load_dotenv
from email.message import EmailMessage
from django.core.mail import EmailMessage

load_dotenv()
env = os.getenv

def send_email(data):
    email=EmailMessage(
        subject=data['subject'],
        body=data['body'],
        from_email=env('MAIL_FROM'),
        to=data['to_email'] if type(data['to_email']) == list else [data['to_email']],
        cc=data['cc']
        
    )
    attachment = data.get('attachment')
    if attachment:
        email.attach(attachment['filename'], attachment['content'], attachment['mimetype'])
    email.send()

def send_email(data):
    email = EmailMessage(
        subject=data['subject'],
        body=data['body'],
        from_email=os.environ.get('EMAIL_USER'),
        to=data['to_email'] if type(data['to_email']) == list else [data['to_email']],
        cc=data['cc']
    )
    attachment = data.get('attachment')
    if attachment:
        email.attach(attachment['filename'], attachment['content'], attachment['mimetype'])

    def _send_email():
        email.send()
    t = threading.Thread(target=_send_email)
    t.start()
                             
def creating_folder(file_type):
    a=''
    if file_type == '1':
        a='Submitted_files'
    elif file_type == '2':
        a='Completed_files'
    elif file_type == '3':
        a = 'Logo_files'
    elif file_type == '4':
        a = 'EPS_files'
    elif file_type == '5':
        a = 'Chat_files'
    return a

def upload_Files(media_blob,file_type,job_id):
    List_file_url = []
    client = boto3.client('s3',
    endpoint_url=settings.AWS_MAIN_S3_ENDPOINT_URL,
    **settings.MEDIA_UPLOAD_AUTH
    )
    transfer = S3Transfer(client)
    current_year = datetime.datetime.now().strftime('%Y')
    current_month = datetime.datetime.now().strftime('%m')
    current_day = datetime.datetime.now().strftime('%d')
    a=creating_folder(file_type)
    media_blob = media_blob if type(media_blob) == list else [media_blob]
    for media in media_blob:
        file_full_path = default_storage.save(media.name, media)
        file_location_url = default_storage.open(file_full_path, 'r')
        key = "{}/{}/{}/{}/{}/{}/{}/{}".format(env('PROJECT_NAME'),env('S3_FOLDER_CLIENT_NAME'),current_year,current_month,current_day,job_id,a,file_full_path)  # set the key for the S3 object
        transfer.upload_file(str(file_location_url), settings.LINODE_BUCKET, key, extra_args={'ACL': 'private'})
        file_location_url.close()
        file_url = '%s/%s'%(settings.AWS_S3_ENDPOINT_URL , key)
        default_storage.delete(file_full_path)
        List_file_url.append(key)
    return List_file_url

def delete_file(file_urls):
    client = boto3.client('s3',
    endpoint_url=settings.AWS_MAIN_S3_ENDPOINT_URL,
    **settings.MEDIA_UPLOAD_AUTH,
    config=boto3.session.Config(signature_version='s3v4')
    )
    boto3.set_stream_logger('')
    bucket_name = settings.LINODE_BUCKET
    if type(file_urls)==list:
        for file_url in file_urls:
            object_key = file_url
            obj=client.delete_object(Bucket = bucket_name,Key = object_key)
    elif type(file_urls) == str:
        obj=client.delete_object(Bucket = bucket_name,Key = file_urls)
