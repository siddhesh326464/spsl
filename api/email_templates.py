from dotenv import load_dotenv
import os
load_dotenv()
env = os.getenv
client_name = env('CLIENT_NAME')

NEW_JOB_SUBJECT = "New Job # {} and Quote# {}"
NEW_JOB_BODY = """
Greetings,

New Job # {} has been added in the system.

Thank you.

Regards,

{} Art Team
"""

JOB_COMPLETED_SUBJECT = "{} - Art completed for Req# {} and Quote# {}"
JOB_COMPLETED_BODY = """
Greetings,

We have completed the virtual for a Quote # {} and completed files are attached for you reference.
Thank you.

Regards,

{} Art Team

"""

NEED_CORRECTION_SUBJECT = "Job # {} and Quote# {} Need corrections"
NEED_CORRECTION_BODY="""
Greetings,

There is a Quote # {} in corrections. Please review and reply.

Thank you.

Regards,

{} Art Team
"""

IN_QUERY_SUBJECT = "Job # {} and Quote# {} is in Query"
IN_QUERY_BODY = """
Greetings,

There is a Quote # {} job in query. Please review and reply.

Regards,

{} Art Team
"""

QUERIES_RESOLVED_SUBJECT = "Job # {} and Quote# {} Queries Resolved"
QUERIES_RESOLVED_BODY = """
Greetings,

Query has been resolved for the Quote # {} . Please review and do the needful.

Thank you.

Regards,

{} Art Team
"""
CUSTOMER_APPROVED_SUBJECT = "Job # {} and Quote# {} is in Customer Approved"
CUSTOMER_APPROVED_BODY = """
Greetings,

The virtual for a Quote # {} is moved to Customer Approved.

Thank you.

Regards,

{} Art Team
"""

CHAT_MESSAGE_SUBJECT= "Job # {} and Quote# {}"
CHAT_MESSAGE_BODY = """
Greetings,

Message - {}.

{}

Thank you.

Regards,

{} Art Team
"""
ATTACHMENT = """attachment - {}."""