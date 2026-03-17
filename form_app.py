# form_app.py - Modular signup form application
# Reusable functions for rendering and processing forms

import os
import csv
import threading
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st


class SignupForm:
    """A modular signup form manager that handles form rendering and data persistence."""

    def __init__(self, config):
        """
        Initialize the form with a configuration dictionary.
        
        Args:
            config: Configuration dict with EVENT, FORM_FIELDS, CSV_COLUMNS, 
                   TIMEZONE, DATA_DIR, CSV_FILENAME
        """
        self.config = config
        self.data_dir = config["DATA_DIR"]
        self.csv_path = os.path.join(self.data_dir, config["CSV_FILENAME"])
        self.timezone = config["TIMEZONE"]
        self.columns = config["CSV_COLUMNS"]
        self.form_fields = config["FORM_FIELDS"]
        
        os.makedirs(self.data_dir, exist_ok=True)
        self._write_lock = threading.Lock()

    def render_page_header(self):
        """Render the page title and event description."""
        event = self.config["EVENT"]
        st.set_page_config(
            page_title=event["title"],
            page_icon=event["icon"],
            layout="centered"
        )
        st.title(event["title"])
        st.write(event["description"])
        
        # Show event details if available
        if "EVENT_DETAILS" in self.config:
            details = self.config["EVENT_DETAILS"]
            st.info(
                f"**Location:** {details['location']}\n\n"
                f"**Date:** {details['date']}\n\n"
                f"**Time:** {details['play_time']}\n\n"
                f"**Travel Time:** {details['travel_time']} each way"
            )

    def render_form(self):
        """
        Render the dynamic form based on FORM_FIELDS configuration.
        
        Returns:
            dict: Form data if submitted, None otherwise
        """
        with st.form("signup", clear_on_submit=True):
            form_data = {}
            
            for field in self.form_fields:
                key = field["key"]
                name = field.get("name", key)
                field_type = field.get("type", "text")
                required = field.get("required", True)
                
                if field_type == "text":
                    placeholder = field.get("placeholder", "")
                    form_data[key] = st.text_input(
                        name,
                        placeholder=placeholder
                    )
                
                elif field_type == "radio":
                    options = field.get("options", [])
                    form_data[key] = st.radio(
                        name,
                        options=options,
                        horizontal=field.get("horizontal", False)
                    )
                
                elif field_type == "checkbox":
                    form_data[key] = st.checkbox(name)
                
                elif field_type == "textarea":
                    placeholder = field.get("placeholder", "")
                    form_data[key] = st.text_area(
                        name,
                        placeholder=placeholder
                    )
            
            submitted = st.form_submit_button("Submit")
        
        return form_data if submitted else None

    def validate_submission(self, form_data):
        """
        Validate form submission based on field requirements.
        
        Args:
            form_data: Dictionary of form data
            
        Returns:
            bool: True if valid, False otherwise
        """
        for field in self.form_fields:
            if field.get("required", True):
                key = field["key"]
                value = form_data.get(key, "").strip()
                if not value:
                    st.error(f"{field['name']} is required.")
                    return False
        
        return True

    def append_row(self, row_dict):
        """
        Append a row to the CSV file.
        
        Args:
            row_dict: Dictionary of data to append
        """
        is_new = not os.path.exists(self.csv_path) or os.path.getsize(self.csv_path) == 0
        with self._write_lock:
            with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.columns)
                if is_new:
                    writer.writeheader()
                # Only write configured columns
                writer.writerow({k: row_dict.get(k, "") for k in self.columns})

    def process_submission(self, form_data):
        """
        Process and save form submission.
        
        Args:
            form_data: Dictionary of form data
        """
        if not self.validate_submission(form_data):
            st.stop()

        row = {k: form_data[k].strip() if isinstance(form_data[k], str) else form_data[k]
               for k in form_data}
        row["SubmittedAt"] = datetime.now(ZoneInfo(self.timezone)).strftime("%Y-%m-%d %H:%M:%S")

        try:
            self.append_row(row)
            st.success("Thank you! Your submission has been recorded.")
        except Exception as e:
            st.error(f"Could not save your submission: {e}")

    def display_recent_submissions(self, limit=10):
        """
        Display recent submissions in a table.
        
        Args:
            limit: Number of recent submissions to display
        """
        st.divider()
        st.subheader("Recent submissions")

        if os.path.exists(self.csv_path):
            try:
                with open(self.csv_path, newline="", encoding="utf-8") as f:
                    rows = list(csv.DictReader(f))
                if rows:
                    st.dataframe(rows[-limit:], use_container_width=True)
                else:
                    st.info("No submissions yet.")
            except Exception as e:
                st.warning(f"Unable to load preview: {e}")
        else:
            st.info("No submissions yet.")


def run_form_app(config):
    """
    Run the signup form application.
    
    Args:
        config: Configuration dictionary with all needed settings
    """
    form = SignupForm(config)
    form.render_page_header()
    
    form_data = form.render_form()
    if form_data:
        form.process_submission(form_data)
    
    form.display_recent_submissions()
