from ics import Calendar, Event

def create_google_maps_embed(location):
    """
    Creates a Google Maps embed URL for a given location.

    Args:
        location (str): The location to embed.

    Returns:
        A string containing the Google Maps embed URL.
    """
    # Mocking Google Maps API for testing purposes
    # In a real application, you would use a valid API key and handle geocoding properly.
    return f"https://maps.google.com/maps?q={location}"

def create_ics_file(summary, dtstart, dtend):
    """
    Creates an ICS file for a given event.

    Args:
        summary (str): The summary of the event.
        dtstart (datetime): The start time of the event.
        dtend (datetime): The end time of the event.

    Returns:
        A string containing the ICS file.
    """
    c = Calendar()
    e = Event()
    e.name = summary
    e.begin = dtstart
    e.end = dtend
    c.events.add(e)
    return str(c)

def send_reminder(to_email, subject, body):
    """
    Sends an email reminder using a placeholder. In a real application,
    this would integrate with SendGrid or Twilio SendGrid.
    """
    print(f"Sending email to {to_email} with subject '{subject}' and body '{body}'")
    return {"status": "success", "message": "Reminder sent (placeholder)"}
