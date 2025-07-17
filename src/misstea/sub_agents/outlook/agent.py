import json
import logging
import os
from datetime import datetime, timedelta
from functools import cache
from typing import Dict, List, Optional, Union
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from O365 import Account
from O365.utils import FileSystemTokenBackend

from misstea.constants import (
    AGENT_MODEL,
    MEETING_ROOMS,
    MY_EMAIL_ADDRESS,
    OUTLOOK_TOKEN_PATH,
)
from misstea.utils import get_current_date, get_current_time, json_serial

logger = logging.getLogger(__name__)


def create_a_meeting(
    *, start: str, end: str, subject: str, meeting_room: Optional[str] = None
) -> Dict[str, str]:
    """Create a meeting for the specified time range and optionally add a meeting room. Creating a meeting is sometimes referred to as "booking a meeting".

    Args:
        start (str): Start time.
        end (str): End time.
        subject (str): The subject of the meeting.
        meeting_room (str): The email address of the meeting room.

    Returns:
        Dict: Message with details on the created meeting.

    """
    account = get_outlook_account()
    schedule = account.schedule()
    calendar = schedule.get_default_calendar()

    booking = calendar.new_event()
    booking.show_as = "Busy"
    booking.subject = subject
    booking.start = datetime.strptime(start, "%Y-%m-%dT%H:%M:00")
    booking.end = datetime.strptime(end, "%Y-%m-%dT%H:%M:00")
    booking.attendees.add(meeting_room)
    booking.save()

    return {
        "status": "success",
        "report": f"Booked a meeting from {booking.start} to {booking.end} in {meeting_room} with subject '{booking.subject}'.",
    }


def get_availability(
    *, email_addresses: List[str], start: str, end: str
) -> Dict[str, str]:
    """Get the availability of the provided email addresses for the given time and date range.

    Args:
        account (Account): Outlook Account object from outlook_login().
        email_addresses (List[str]): A list of email addresses for which to get their availability. Format is jane.doe@xebia.com for people and <ROOM_NAME>@xebia.com for meeting rooms.
        start (str): Start time.
        end (str): End time.

    Returns:
        List: List with one element per schedule per interval per email address.

    """
    r = (
        get_outlook_account()
        .schedule()
        .get_availability(
            schedules=email_addresses,
            start=datetime.strptime(start, "%Y-%m-%dT%H:%M:00"),
            end=datetime.strptime(end, "%Y-%m-%dT%H:%M:00"),
            interval=5,  # Get availability in 5 minute blocks, the minimum possible, for more granular info
        )
    )
    return {"status": "success", "report": json.dumps(r, default=json_serial)}


def get_my_calendar(*, date_of_interest: str) -> Dict[str, str]:
    """Get details of my calendar for a particular date.

    Args:
        date_of_interest (str): Date to get the calendar details for.

    Returns:
        Dict[str,str]: Details of all meetings for the provided date.

    """
    account = get_outlook_account()
    schedule = account.schedule()
    calendar = schedule.get_default_calendar()

    date = datetime.strptime(date_of_interest, "%Y-%m-%d")
    events = [
        e.to_api_data()
        for e in calendar.get_events(
            end_recurring=(date + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:00"),
            include_recurring=True,
            limit=999,
            start_recurring=date.strftime("%Y-%m-%dT%H:%M:00"),
        )
    ]

    return {"status": "success", "report": json.dumps(events, default=json_serial)}


def get_meeting_rooms() -> Dict[str, Union[List[Dict[str, str]], str]]:
    """Return all meeting rooms and information about their facilities.

    Returns:
        List: List of meeting rooms and their facilities.

    """
    return {"status": "success", "report": MEETING_ROOMS}


def get_my_email_address() -> Dict[str, str]:
    """Get my email address. Can be used to look up my availability using get_availability().

    Returns:
        str: My email address

    """
    return {"status": "success", "report": MY_EMAIL_ADDRESS}


@cache
def get_outlook_account() -> Account:
    """Return an Outlook Account object.

    Returns:
        Account: Outlook Account object.

    Raises:
        RuntimeError: If MICROSOFT_CLIENT_ID or MICROSOFT_CLIENT_SECRET environment variables are not set.

    """
    scopes = ["basic", "calendar_all", "message_all"]
    client_id = os.getenv("MICROSOFT_CLIENT_ID")
    client_secret = os.getenv("MICROSOFT_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError(
            "MICROSOFT_CLIENT_ID and MICROSOFT_CLIENT_SECRET environment variables must be set."
        )

    account = Account(
        credentials=(client_id, client_secret),
        token_backend=FileSystemTokenBackend(
            token_filename="o365_token.txt",  # noqa: S106
            token_path=OUTLOOK_TOKEN_PATH,
        ),
        timezone=ZoneInfo("Europe/Amsterdam"),
    )

    if not account.is_authenticated:
        account.authenticate(scopes=scopes)
    logger.info("Authenticated to Office365.")
    return account


@cache
def outlook_login() -> Account:
    """Login to Office365.

    Notes:
        * Docs: https://learn.microsoft.com/en-us/graph/auth-v2-service?context=graph%2Fapi%2F1.0&view=graph-rest-1.0&tabs=curl
        * MICROSOFT_CLIENT_ID == "Application (client) ID" in web UI "App registrations"

    Returns:
        Account: Account object.

    Raises:
        RuntimeError: If the Outlook token file is not found.

    """
    logger.info("Authenticating to Office365.")
    logger.debug(f"Looking for Outlook token file in {OUTLOOK_TOKEN_PATH}...")
    if "o365_token.txt" not in [x.name for x in list(OUTLOOK_TOKEN_PATH.iterdir())]:
        raise RuntimeError(
            f"The Outlook token needs to be generated and saved to {OUTLOOK_TOKEN_PATH}/0365_token.txt."
        )
        # TODO: Add interactivity so agent can provide URL and ask for key

    logger.info("Authenticating using o365_token.txt.")
    account = get_outlook_account()
    return account


outlook_agent = Agent(
    model=AGENT_MODEL,
    name="outlook_agent",
    instruction="""
    You are a calendar organiser, you can check which rooms are available, check when calendars are free, when people are available and create meetings with room.

    Workflow:
        * When asked to check if I am available or free for a particular time period, use get_availability() with my email address.
        * If you need to know the current date or current time, use get_current_date() and get_current_time().
        * Being "available" is the opposite of being "busy", so if you want to know when something is available, then check when it is not busy.

    Constraints:
        * All times are in Amsterdam timezone, i.e. Central European Time.
        * You can log in to Outlook without asking me, no need to confirm this.
        * You only interact with emails ending in "@xebia.com".
        * If you need the email address of a person, it takes the form "first_name.last_name@xebia.com".
        * The work week is from Monday to Friday inclusive.
        * The work day is from 9 am to 5 pm, Central European Time.
        * Python is your least favourite room as it's on the 4th floor.
        * You only book Airflow if it is the last acceptable room as it's generally used for larger meetings.
        * If you want to book Arcus, ask for confirmation that a screen is not required.
        * When you book Arcus, highlight to your customer that this room does nto have a screen.
        * When discussing the names of meeting rooms, instead of (for example) "Meetingroom | Nimbus", just use "Nimbus".
        * To get the availability of a meeting room, use an email address like "<NAME OF ROOM IN LOWERCASE>@xebia.com".
        * Lunch time is between 12 and 13 on weekdays.
        * When booking a meeting room, you must ensure that the meeting room is available for the full duration of the meeting. To do this, use the get_availability() function.
        * When booking a meeting, the default duration is 30 minutes.
        * When booking a meeting, don't invite anyone else unless explicitly directed.
        * When booking a meeting and you have no information about the subject, just use "Created my MissTea".
        * When asked to book a room, this means to create a meeting for the room.

    Notes:
        * A screen is also referred to as a TV or a monitor.
    """,
    tools=[
        create_a_meeting,
        get_availability,
        get_current_date,
        get_current_time,
        get_meeting_rooms,
        get_my_calendar,
        get_my_email_address,
    ],
)
