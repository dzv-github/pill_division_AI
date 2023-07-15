import requests
import os

# Shutterstock API credentials
client_id = 'ZJ7IGb5fjew1Qd31FRD4wQ5F1reWLHZS'
client_secret = 'lXsgzsKtIkEj9uAI'

# Search parameters
search_query = 'bead'
image_count = 100  # Number of images to retrieve
image_folder = 'PlasticBead_images'  # Folder to save the downloaded images

# Create the folder to save images
os.makedirs(image_folder, exist_ok=True)

# Shutterstock API endpoints
auth_url = 'https://api.shutterstock.com/v2/oauth/access_token'
search_url = 'https://api.shutterstock.com/v2/images/search'

# Obtain access token
auth_data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials'
}

auth_response = requests.post(auth_url, data=auth_data)

if auth_response.status_code == 200:
    access_token = auth_response.json().get('access_token')
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Search for images
    params = {
        'query': search_query,
        'per_page': image_count
    }

    search_response = requests.get(search_url, params=params, headers=headers)

    if search_response.status_code == 200:
        image_data = search_response.json().get('data')

        # Download and save each image
        for i, image in enumerate(image_data):
            image_url = image['assets']['preview']['url']
            image_extension = image_url.split('.')[-1]
            image_filename = f'image_{i+1}.{image_extension}'
            image_path = os.path.join(image_folder, image_filename)

            # Download the image
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)
            else:
                print(f"Failed to download image {i+1}")

        print(f"Downloaded {len(image_data)} images to '{image_folder}'")
    else:
        print("Search request failed.")
else:
    print("Authentication failed.")