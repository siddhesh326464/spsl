def set_cookies(response,token):
    response.set_cookie('refresh_token', token['refresh'].replace('Bearer','').strip())
    response.set_cookie('access_token', token['access'].replace('Bearer','').strip())
    return response

def get_cookies(request):
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    return access_token,refresh_token