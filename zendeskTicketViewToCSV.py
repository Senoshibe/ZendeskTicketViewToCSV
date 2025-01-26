import requests
import csv
import os

# Settings
ZENDESK_API_TOKEN = os.getenv('ZENDESK_API_TOKEN')  # Load the API token from an environment variable for security
ZENDESK_USER_EMAIL = 'ken.choi@mortgagechoice.com.au'
ZENDESK_SUBDOMAIN = 'mortgagechoice'

view_tickets = []
view_id = '42792217899161'

auth = f'{ZENDESK_USER_EMAIL}/token', ZENDESK_API_TOKEN

print(f'Getting tickets from view ID {view_id}')
url = f'{ZENDESK_SUBDOMAIN}/api/v2/views/{view_id}/tickets.json'
while url:
    response = requests.get(url, auth=auth) 
    if response.status_code == 200:
        page_data = response.json()
        tickets = page_data['tickets']
        view_tickets.extend(tickets)
        url = page_data['next_page']
    else:
        print(f"Failed to retrieve tickets: {response.reason}")
        url = None  # Exit loop on failure

rows = [('Ticket ID', 'Requester', 'Assignee', 'Status', 'Subject', 'Description', 'Last Updated', 'Ticket URL')]

for ticket in view_tickets:
    row = (
        ticket['id'],
        ticket['requester'],
        ticket['assignee_email'],
        ticket['status'],
        ticket['subject'],
        ticket['description'],
        ticket['updated_at'],
        ticket['url'],
        f'https://{ZENDESK_SUBDOMAIN}.zendesk.com/agent/tickets/{ticket["id"]}'
    )
    rows.append(row)

with open('crowdstrike_tickets.csv', mode='w', newline='') as csv_file:
   report_writer = csv.writer(csv_file, dialect='excel')
   for row in rows:
       report_writer.writerow(row)