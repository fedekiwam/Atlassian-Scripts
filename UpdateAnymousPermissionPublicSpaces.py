import requests
import json
import base64
import csv

# Confluence Cloud server details
confluence_base_url = 'PUT ATLASSIAN URL HERE'  # Replace with your Confluence Cloud site URL - without the wiki word
username = 'PUT YOUR USERNAME HERE'  # Replace with your Confluence Cloud username
password = 'PUT YOUR API TOKEN HERE'  # Replace with your API token - https://id.atlassian.com/manage-profile/security/api-tokens

# Encode the username and api token as base64
credentials = base64.b64encode(f'{username}:{password}'.encode()).decode()

# Set up headers with basic authentication
headers = {
    'Authorization': f'Basic {credentials}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# Read space keys from the CSV file downloaded
with open('Name&PathofTheFileHere.csv', mode='r') as csv_file:   # Remember to change the path where the CSV file exist
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row if present
    for row in csv_reader:
        space_key = row[0].strip()  # Assuming the space keys are in the first column of the CSV, remove leading/trailing spaces

        # Get the space details to check the current permissions
        space_url = f'{confluence_base_url}wiki/rest/api/space/{space_key}?expand=permissions'

        try:
            response = requests.get(space_url, headers=headers)

            if response.status_code != 200:
                print(f'Failed to retrieve space details for space key {space_key}. Status code: {response.status_code}')
                continue  # Continue to the next space key

            # Check the content type of the response
            content_type = response.headers.get('content-type', '')

            if 'application/json' in content_type:
                space_details = response.json()

                # Check if 'anonymousAccess' is true and update it if needed
                if 'permissions' in space_details:
                    for permission in space_details['permissions']:
                        if permission.get('anonymousAccess') is True:
                            # Send a DELETE request to remove this permission
                            delete_url = f'{confluence_base_url}wiki/rest/api/space/{space_key}/permission/{permission["id"]}'
                            response = requests.delete(delete_url, headers=headers)

                            if response.status_code == 204:
                                print(f'Removed permission {permission["id"]} successfully for space key {space_key}.')
                            else:
                                print(f'Failed to remove permission {permission["id"]} for space key {space_key}. Status code: {response.status_code}')
                else:
                    print(f'No permissions found in space details for space key {space_key}.')
            else:
                print(f'Response content is not in JSON format (Content-Type: {content_type}).')

        except Exception as e:
            print(f'An error occurred for space key {space_key}: {str(e)}')
