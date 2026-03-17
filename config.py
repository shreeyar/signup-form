# config.py - Event configuration for signup forms
# Easily customize this file to change events and form fields

# Event Details
EVENT = {
    "title": "Topgolf Sign-Up",
    "description": "Interested in going to Topgolf in Auburn Hills? Sign up below!",
    "icon": "⛳",
}

# Location and Time Details
EVENT_DETAILS = {
    "location": "Topgolf, Auburn Hills",
    "date": "Tuesday, April 14th",
    "play_time": "6:00 PM - 8:30 PM",
    "travel_time": "1.5 hours each way",
}

# Form Fields Configuration
# Each field is a dict with:
# - "name": display name for the field
# - "type": "text", "radio", "checkbox", "textarea"
# - "placeholder": placeholder text (optional)
# - "options": list of options for radio/checkbox (optional)
# - "required": whether this field is required (default: True)
FORM_FIELDS = [
    {
        "key": "Name",
        "name": "Full Name",
        "type": "text",
        "placeholder": "Jane Doe",
        "required": True,
    },
    {
        "key": "Going",
        "name": "Are you going?",
        "type": "radio",
        "options": ["Yes", "No"],
        "horizontal": True,
        "required": True,
    },
]

# CSV Configuration
# Defines the columns in the output CSV file
CSV_COLUMNS = ["Name", "Going", "SubmittedAt"]

# Email Configuration
# Email address to receive submissions
RECIPIENT_EMAIL = "shreramesh@deloitte.com"

# Timezone for submissions
TIMEZONE = "America/Detroit"

# Data directory
DATA_DIR = "data"
CSV_FILENAME = "topgolf_submissions.csv"
