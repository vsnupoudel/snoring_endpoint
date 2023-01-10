import os, requests

def login(request):
    auth = request.authorization
    if not auth:
        return None, ("missing credentials in access", 401)

    basicAuth = (auth.username, auth.password)
    # print("inside access basicAuth:", basicAuth)
    # print("========================================")
    # print( os.environ.get('AUTH_SVC_ADDRESS') )
    # print("========================================")


    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
        auth= basicAuth
)

    # print( response.status_code )
    # print("========================================")
    

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
