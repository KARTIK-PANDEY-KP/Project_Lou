import requests

def fetch_email(body):
    url = "https://api.anymailfinder.com/v5.0/search/linkedin-url.json"
    headers = {
        "Authorization": "Bearer Nz8Oz4n1RIq4dWVtiTzhbS0O",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=body, headers=headers)
        data = response.json()
        status_code = response.status_code

        if status_code == 200:
            results = data['results']
            print(f"Found {results['fullName']} ({results['title']} at {results['companyName']})")
            print(f"Email: {results['email']} ({'verified' if results['validation'] == 'valid' else 'not verified'})")
            return

        if status_code == 400 or status_code == 401:
            print(f"Invalid request: {data['error_explained']}")
        elif status_code == 402:
            print(f"Insufficient credits: {data['error_explained']}")
        elif status_code == 404 or status_code == 451:
            print("Email not found!")
        else:
            print(f"Unknown error: {status_code} {data['error_explained']}")

    except requests.RequestException as error:
        print(f"Request failed: {error}")

# Call the function with example data
fetch_email({
    "linkedin_url": "https://www.linkedin.com/in/satyanadella/"
})