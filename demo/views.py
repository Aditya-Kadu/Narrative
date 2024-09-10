from django.shortcuts import render
from django.http import JsonResponse
from .models import Booking
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime

# Function to display the booking form


def book_demo(request):
    sectors = ['Supply chain', 'Logistics', 'Business ops', 'Revenue ops', 'Data analytics',
               'Finance', 'Customer success', 'Account management', 'Customer support', 'HR', 'Sales']
    return render(request, 'book_demo.html', {'sectors': sectors})

# Function to fetch available slots from Google Calendar


def get_available_slots(request):
    calendar_id = 'ceo@narrative.com'
    creds = Credentials.from_authorized_user_info(
        request.session['google_credentials'])
    service = build('calendar', 'v3', credentials=creds)

    # Set the time range (next 7 days)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    end = (datetime.datetime.utcnow() +
           datetime.timedelta(days=7)).isoformat() + 'Z'

    events_result = service.events().list(calendarId=calendar_id, timeMin=now, timeMax=end,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    available_slots = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        available_slots.append({'start': start, 'end': end})

    return JsonResponse(available_slots, safe=False)

# Function to confirm booking


def confirm_booking(request):
    if request.method == 'POST':
        sector = request.POST['sector']
        selected_slot = request.POST['selected_slot']
        client_email = request.POST['email']

        # Save the booking
        booking = Booking(sector=sector, time_slot=selected_slot,
                          client_email=client_email)
        booking.save()

        # Send email notification (or further processing)
        # send_email_notification(booking)

        return JsonResponse({'status': 'success', 'message': 'Booking confirmed'})
