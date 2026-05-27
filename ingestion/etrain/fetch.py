import requests

def fetch_html(session: requests.Session,url):
    response = session.get(url,allow_redirects=True, timeout=15)
    response.raise_for_status() #have to update the response code inside error handling
    #so reutns only if success
    return {
        "html":response.text,
        "status_code": response.status_code,
        "final_url": str(response.url)
    }
   