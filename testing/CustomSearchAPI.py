import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

with build('drive', 'v3') as service:
    request = service.stamps().list(cents=5)
    try:
        response = request.execute()
    except HttpError as e:
        print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

    print(json.dumps(response, sort_keys=True, indent=4))
