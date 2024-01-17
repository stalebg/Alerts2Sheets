import json
import gspread
import feedparser
import google.oauth2
from datetime import datetime
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

google_credentials = config['google_credentials']
master_config_url = config['master_config_url']

# Initialize Google Sheets client
gc = gspread.service_account_from_dict(google_credentials)

def get_worksheet(sheet_url):
    # Get the first worksheet of a Google Sheet document by its URL. 
    sh = gc.open_by_url(sheet_url)
    return sh.sheet1

def write_to_google_sheets(worksheet, master_worksheet, row_index, published_date, title, summary, url):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    row = [current_date, current_time, url, title, summary, published_date]

    # Check for duplicates
    existing_rows = worksheet.get_all_values()[1:]  # Exclude header
    for existing_row in existing_rows:
        if existing_row[2] == url:  # Assuming URLs are in the 3rd column
            print(f'Skipping duplicate entry: {url}')
            return

    # Add new row to worksheet
    worksheet.append_row(row)
    print(f'Added new entry to Google Sheets: {title}')

    # Update 'Last Update' in master sheet
    last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Update the 4th column (Last Update) of the master sheet
    master_worksheet.update_cell(row_index, 4, last_update_time)

def fetch_rss_feed(feed_url):
    # Fetch and parse the RSS feed. 
    return feedparser.parse(feed_url)

def update_last_update_in_master_sheet(master_worksheet, row_number, last_update_time):
    # Update the 'Last Update' column for the specific row in the master sheet.
    master_worksheet.update_cell(row_number, 4, last_update_time)

def get_feed_config(master_sheet_url):
    # Get the RSS feed and corresponding sheet configuration from the master sheet.
    sh = gc.open_by_url(master_sheet_url)
    worksheet = sh.sheet1
    return worksheet.get_all_records()

# Get feed and sheet configuration
master_worksheet = gc.open_by_url(master_config_url).sheet1
feed_config_list = get_feed_config(master_config_url)

print("Script started...")

# Loop through feed configurations
for index, feed_config in enumerate(feed_config_list, start=2):  # Assuming the first feed is on row 2
    feed_url = feed_config['RSS Feed URL']
    sheet_url = feed_config['Google Sheet URL']

    worksheet = get_worksheet(sheet_url)

    print(f'\nScanning feed: {feed_url}')
    feed = fetch_rss_feed(feed_url)
    for entry in feed.entries:
        title = entry.title
        summary = entry.summary
        url = entry.link
        published_date = entry.get('published', datetime.now().strftime("%Y-%m-%d"))
        
        # Pass master_worksheet and row_index to the function
        write_to_google_sheets(worksheet, master_worksheet, index, published_date, title, summary, url)

print(f'\nFinished scanning all feeds.')