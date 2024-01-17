# Alerts2Sheets
![License](https://img.shields.io/badge/License-MIT-green)
![Heroku](https://img.shields.io/badge/Heroku-purple?logo=heroku&amp;logoColor=white)

Your Google Alert (as RSS updates) logged in desired Google Sheets. Heroku ready.

## Overview 📜
This script is a parses a list of RSS feeds (designed for Google Alerts) and updates specified Google Sheets documents with the latest information. For simplicity, the script uses a master configuration sheet, where you quickly can specify the feed sources and their corresponding output destinations.

## Features 🔍
- **RSS Feed Parsing**: Processes multiple RSS feeds, extracting key details such as date, title, summary, and URL.
- **Google Sheets Integration**: Writes parsed data to specified Google Sheets.
- **Duplicate Avoidance**: Incorporates a mechanism to prevent duplicate entries.
- **Dynamic Configuration**: Uses one Google Sheet to manage feed URLs and corresponding output Sheets.
- **Last Update Tracking**: Updates the master configuration sheet with the timestamp of the last successful data entry, enabling a quick overview of which feeds are being updated.
- **Heroku Ready**: All files neccesary to run at scheduled intervals via Heroku are included.

## Setup and Configuration 🛠️
### Prerequisites
- Python 3.x
- Access to Google Sheets API and a Google Service Account
- Installed Python libraries: `gspread`, `feedparser`,`oauth2`

### Configuration Steps
1. **Google Service Account**: Ensure you have a Google Service Account with Sheets API enabled. Download the credentials JSON file. If you're unfamiliar with this process, follow the steps outlined in [this tutorial](https://aryanirani123.medium.com/read-and-write-data-in-google-sheets-using-python-and-the-google-sheets-api-6e206a242f20).
2. **Master Configuration Sheet**: Create a Google Sheet with columns for "Alert Name", "RSS Feed URL", and "Google Sheet URL". Share this sheet with your service account.

| Alert Name  |  RSS Feed URL | Google Sheet URL  |
| ------------ | ------------ | ------------ |
|   |   |   |

3. **config.json**: Create a `config.json` file with your Google Service Account credentials and the URL of the Master Configuration Sheet. An example of what it looks like below and in the included `config.json`-file.

```json
{
"google_credentials": {
    "type": "ACCOUNT TYPE",
    "project_id": "PROJECT NAME",
    "private_key_id": "PRIVATE KEY",
    "private_key": "-----BEGIN PRIVATE KEY-----LONG KEY-----END PRIVATE KEY-----",
    "client_email": "ACCOUNT EMAIL",
    "client_id": "NUMBER",
    "auth_uri": "AUTH-URL",
    "token_uri": "TOKEN-URL",
    "auth_provider_x509_cert_url": "AUTH-PROVIDER-URL",
    "client_x509_cert_url": "CLIENT-CERT-URL"
}
"master_config_url": "URL of your Master Configuration Sheet"
}
```

## Use 📘

Run the script using Python. All files nessecary to deploy directly on Heroku are included.

Upon running, the script will automatically:

1. Read the RSS feed URLs and their corresponding Google Sheets URLs from your master configuration sheet.
2. Parse each RSS feed, extract relevant information, and write it to its designated Google Sheet.
3. Update the "Last Update" column in the master sheet upon successful addition of new data.

## Limitations and Considerations 🚧

- Performance may vary based on the number of feeds and the size of the Google Sheets. For large datasets, consider a more advanced solutions.
- The script currently assumes unique URLs across all feeds. If the same URL appears in different feeds, it might be treated as a duplicate.
- Ensure your Google Service Account has the necessary permissions to access and edit all specified Google Sheets.
