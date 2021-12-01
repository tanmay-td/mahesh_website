
import requests

def send_msg(sms,number):
    
    url = "https://www.fast2sms.com/dev/bulkV2"
    

    payload = "message={}&language=english&route=q&numbers={}".format(sms,number)

    headers = {
        'authorization': "JAbCjpEy3KqgzkW10BXZ8lS9M4OfsRr7Vn6cLDNeGdvQtwuxmFQkNEM2q59VZergtuHAs7CX3cjmvGo1",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)