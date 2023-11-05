from rest_framework import status

messages = {
    1002: {
        "error": {"status_code": 4002, "msg": "Account creation request has already been initiated"},
        "status": status.HTTP_401_UNAUTHORIZED
    },
    1003: {
        "error": {"status_code": 1003, "msg": "OOps! Something went wrong"},
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR
    },
    1004: {
        "error": {"status_code": 4004, "msg": "Username or Password doesn't match..!"},
        "status": status.HTTP_401_UNAUTHORIZED
    },
    1005: {
        "error": {"status_code": 1005, "msg": "Invalid refresh token"},
        "status": status.HTTP_400_BAD_REQUEST
    },
    2001:{
        "error":{"status_code":2001,"msg":"Sorry, I couldn’t found any job for this no.!"},
        "status":status.HTTP_404_NOT_FOUND
    },
    2002:{
        "error": {"status_code":2002,"msg":"You are not a autharized user"},
        "status":status.HTTP_401_UNAUTHORIZED
    },
    2003:{
        "error":{"status_code":2003,"msg":"Sorry, I couldn’t found any job for this status.!"},
        "status":status.HTTP_404_NOT_FOUND
    },
    2004:{
        "error":{"status_code":2004,"msg":"Something went wrong while sending mail"},
        "status":status.HTTP_404_NOT_FOUND
    },
    2005:{
        "error":{"status_code":2005,"msg":"Invalid choice.!"},
        "status":status.HTTP_405_METHOD_NOT_ALLOWED
    },
   2006:{
       "error":{"status_code":2006,"msg":"Invalid choice for status"},
       "status":status.HTTP_404_NOT_FOUND
   },
   2007:{
       "error":{"status_code":2007,"msg":"Invalid choice for Proof request type"},
       "status":status.HTTP_404_NOT_FOUND
   },
   2008:{
       "error":{"status_code":2007,"msg":"Sorry, I couldn’t found any jobitemlist for this no.!"},
       "status":status.HTTP_404_NOT_FOUND
   },
   2009:{
       "error":{"status-code":2009,"msg":"Sorry you are not authorized  to upaload this type of file"},
       "status":status.HTTP_401_UNAUTHORIZED
   },
   2010:{
       "error":{"status-code":2010 , "msg":"you are not authorized to update job"},
       "status":status.HTTP_401_UNAUTHORIZED
   },
   2011:{
       "error":{"status_code":2011 , "msg":"you are not authorized to see this job"},
       "status":status.HTTP_401_UNAUTHORIZED
   },
   2012:{
       "error":{"status_code":2012 , "msg":"you are not authorized to send message for this job "},
       "status":status.HTTP_401_UNAUTHORIZED
   },
   2013:{
       "error":{"status_code":2013 , "msg":"you are not authorized to send message for this job "},
       "status":status.HTTP_401_UNAUTHORIZED
   },
   2014:{
       "error":{"status_code":2014 , "msg":"unsuported file type"},
       "status":status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
   },
   2015:{
       "error":{"status_code":2015 , "msg":"Sorry, This Item no already deleted!"},
       "status":status.HTTP_404_NOT_FOUND
   },
   2016:{
       "error":{"status_code":2016 , "msg":"Sorry, This file no already deleted!"},
       "status":status.HTTP_404_NOT_FOUND
   },
   2017:{
       "error":{"status_code":2017 , "msg":"No files to deleted "},
       "status":status.HTTP_404_NOT_FOUND
   },
   2018:{
       "error":{"status_code":2017 , "msg":"quote_no must be a string "},
       "status":status.HTTP_404_NOT_FOUND
   },
   2019:{
       "error":{"status_code":2018 , "msg":"logo_same_for_all must be a True or False"},
       "status":status.HTTP_404_NOT_FOUND
   },
   2020:{
       "error":{"status_code":2020 , "msg":"logo_name must be a string"},
       "status":status.HTTP_404_NOT_FOUND
   },
   2021:{
       "error":{"status_code":2021 , "msg":"proof_request_type must be a string "},
       "status":status.HTTP_404_NOT_FOUND
   },
   2022:{
       "error":{"status_code":2022 , "msg":"campaign must be a int "},
       "status":status.HTTP_404_NOT_FOUND
   },
   2023:{
       "error":{"status_code":2023 , "msg":"customer_no must be a string "},
       "status":status.HTTP_404_NOT_FOUND
   },
   2024:{
       "error":{"status_code":2024 , "msg":"segment_no must be a string "},
       "status":status.HTTP_404_NOT_FOUND
   },
   2025:{
       "error":{"status_code":2025 , "msg":"note must be a string"},
       "status":status.HTTP_404_NOT_FOUND
   },
   2026:{
       "error":{"status_code":2026 , "msg":"status must be a string "},
       "status":status.HTTP_404_NOT_FOUND
   },
   2027:{
       "error":{"status_code":2027 , "msg":"item must be a string"},
       "status":status.HTTP_404_NOT_FOUND
   },
   2028:{
       "error":{"status_code":2028 , "msg":"product_color must be a string"},
       "status":status.HTTP_404_NOT_FOUND
   },
   2029:{
       "error":{"status_code":2029 , "msg":"imprint_color must be a string "},
       "status":status.HTTP_404_NOT_FOUND
   },
   2030:{
       "error":{"status_code":2030 , "msg":"imprint_location must be a string"},
       "status":status.HTTP_404_NOT_FOUND
   },
   2031:{
       "error":{"status_code":2031 , "msg":"imprint_method must be a string "},
       "status":status.HTTP_404_NOT_FOUND
   },
   2032:{
       "error":{"status_code":2032 , "msg":"imprint_instructions must be a string"},
       "status":status.HTTP_404_NOT_FOUND
   },
   
   2033:{
       "error":{"status_code":2033 , "msg":"campaign with this name already exists"},
       "status":status.HTTP_409_CONFLICT
   },

   2034:{
       "error":{"status_code":2034 , "msg":"campaign Id does not exists"},
       "status":status.HTTP_409_CONFLICT
   },
   
}