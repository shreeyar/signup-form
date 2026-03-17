# streamlit_app.py — Modular signup form application
# Imports configuration and runs the form

from config import (
    EVENT, EVENT_DETAILS, FORM_FIELDS, CSV_COLUMNS,
    TIMEZONE, DATA_DIR, CSV_FILENAME, RECIPIENT_EMAIL
)
from form_app import run_form_app

# Build configuration dictionary
config = {
    "EVENT": EVENT,
    "EVENT_DETAILS": EVENT_DETAILS,
    "FORM_FIELDS": FORM_FIELDS,
    "CSV_COLUMNS": CSV_COLUMNS,
    "TIMEZONE": TIMEZONE,
    "DATA_DIR": DATA_DIR,
    "CSV_FILENAME": CSV_FILENAME,
    "RECIPIENT_EMAIL": RECIPIENT_EMAIL,
}

# Run the form application
run_form_app(config)
