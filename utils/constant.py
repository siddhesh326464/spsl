API_AUTH = 'Auth'
API_JOB = 'Job'


PROOF_TYPE = [
        ('1','Standard Proof Request'),
        ('2','Apparel Proof Request'),
        ('3','Branded Guideline Request '),
        ('4','Complex Art Request'),
        ('5','Vectorization Logo Request')
    ]

FILE_TYPE = [
    ('1','submitted file'),
    ('2','completed file'),
    ('3','logo file'),
    ('4','eps files'),
    ('5','chat_file')
]
JOB_STATUS = [
    'New', 
    'Inprogress', 
    'Hold', 
    'Query', 
    'Correction', 
    'Rush Correction', 
    'Completed', 
    'Cancelled', 
    'Query Resolved', 
    'Customer Approved',
    'Final Approved'
]

#job status
NEW = 1
INPROGRESS=2
HOLD=3
QUERY=4
CORRECTION=5
RUSH_CORRECTION=6
COMPLETED=7
CANCELED=8
QUERY_RESOLVED=9
CUSTOMER_APPROVED=10
FINAL_APPROVED=11

JOB_STATUS = [
    {'name':'New','value' : NEW},
    {'name':'In Progress','value' : INPROGRESS},
    {'name':'On Hold','value' : HOLD},
    {'name':'Queries','value' : QUERY},
    {'name':'Corrections','value' : CORRECTION},
    {'name':'Rush Corrections','value' : RUSH_CORRECTION},
    {'name':'Completed','value' : COMPLETED},
    {'name':'Cancelled','value' : CANCELED},
    {'name':'Queries Resolved','value' : QUERY_RESOLVED},
    {'name':'Customer Approved','value' : CUSTOMER_APPROVED},
    {'name':'Final Approved','value' : FINAL_APPROVED},
]

file_type = [
    ('1','submitted file'),
    ('2','completed file'),
    ('3','logo file'),
    ('4','eps files')
]


all = 'all'
logo = 'logo'
segment = 'segment'
requestnumber = 'requestnumber'
quote = 'quote'
campaign = 'campaign'
customerno = 'customerno'
customername = 'customername'
repno = 'repno'