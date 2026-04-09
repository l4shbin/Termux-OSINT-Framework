import requests

def check_username(username, site_url):
    target = site_url.format(username)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(target, headers=headers, timeout=7)
        if response.status_code == 200:
            # Beberapa situs mengembalikan 200 tapi isinya "Not Found"
            if "not found" in response.text.lower() or "404" in response.text:
                return False, None
            return True, target
        return False, None
    except:
        return False, None
