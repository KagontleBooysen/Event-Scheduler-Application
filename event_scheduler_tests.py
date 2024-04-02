import unittest
from unittest.mock import patch
from io import StringIO

import datetime

# In-memory storage for events
events = []

# Function to validate date format
def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Function to validate time format
def validate_time(time_text):
    try:
        datetime.datetime.strptime(time_text, '%H:%M')
        return True
    except ValueError:
        return False

# Function to add a new event
def add_event(title, description, date, time):
    if validate_date(date) and validate_time(time):
        events.append({'title': title, 'description': description, 'date': date, 'time': time})
        return True
    else:
        return False

# Function to display all events sorted by date and time
def display_events_sorted():
    if not events:
        return "No events found."
    else:
        sorted_events = sorted(events, key=lambda x: (x['date'], x['time']))
        event_details = []
        for event in sorted_events:
            event_details.append(f"Title: {event['title']}\nDescription: {event['description']}\nDate: {event['date']}\nTime: {event['time']}\n")
        return event_details

# Function to search events by date or keyword in title/description
def search_events(query):
    found_events = [event for event in events if query in event['title'] or query in event['description'] or query == event['date']]
    if found_events:
        event_details = []
        for event in found_events:
            event_details.append(f"Title: {event['title']}\nDescription: {event['description']}\nDate: {event['date']}\nTime: {event['time']}\n")
        return event_details
    else:
        return "No matching events found."

# Function to edit an existing event
def edit_event(title, new_title, new_description, new_date, new_time):
    global events
    for event in events:
        if event['title'] == title:
            if new_title:
                event['title'] = new_title
            if new_description:
                event['description'] = new_description
            if new_date and validate_date(new_date):
                event['date'] = new_date
            if new_time and validate_time(new_time):
                event['time'] = new_time
            return True
    return False

# Function to delete an event
def delete_event(title):
    global events
    updated_events = [event for event in events if event['title'] != title]
    if len(updated_events) < len(events):
        events = updated_events
        return True
    else:
        return False

# Main function to run the application
def main():
    while True:
        print("\nEvent Scheduler\n")
        print("1. Add Event")
        print("2. View Events")
        print("3. Search Events")
        print("4. Edit Event")
        print("5. Delete Event")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter title: ")
            description = input("Enter description: ")
            date = input("Enter date (YYYY-MM-DD): ")
            time = input("Enter time (HH:MM): ")
            if add_event(title, description, date, time):
                print("Event added successfully.")
            else:
                print("Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.")
        elif choice == '2':
            events_list = display_events_sorted()
            if isinstance(events_list, list):
                for event in events_list:
                    print(event)
            else:
                print(events_list)
        elif choice == '3':
            query = input("Enter search query (date or keyword): ")
            events_list = search_events(query)
            if isinstance(events_list, list):
                for event in events_list:
                    print(event)
            else:
                print(events_list)
        elif choice == '4':
            title = input("Enter title of event to edit: ")
            new_title = input("Enter new title (leave blank to keep current): ")
            new_description = input("Enter new description (leave blank to keep current): ")
            new_date = input("Enter new date (YYYY-MM-DD, leave blank to keep current): ")
            new_time = input("Enter new time (HH:MM, leave blank to keep current): ")
            if edit_event(title, new_title, new_description, new_date, new_time):
                print("Event edited successfully.")
            else:
                print("Event not found.")
        elif choice == '5':
            title = input("Enter title of event to delete: ")
            if delete_event(title):
                print("Event deleted successfully.")
            else:
                print("Event not found.")
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Basic unit tests
class TestEventScheduler(unittest.TestCase):
    def setUp(self):
        # Reset events before each test
        global events
        events = []

    def test_add_event(self):
        self.assertTrue(add_event("Meeting", "Team meeting", "2024-04-03", "14:00"))
        self.assertEqual(len(events), 1)

    def test_search_events(self):
        add_event("Meeting", "Team meeting", "2024-04-03", "14:00")
        add_event("Presentation", "Project presentation", "2024-04-04", "10:00")
        self.assertEqual(len(search_events("2024-04-03")), 1)
        self.assertEqual(len(search_events("meeting")), 1)

    def test_edit_event(self):
        add_event("Meeting", "Team meeting", "2024-04-03", "14:00")
        self.assertTrue(edit_event("Meeting", "Meeting with clients", "Client meeting", "2024-04-05", "15:00"))
        self.assertEqual(events[0]['title'], "Meeting with clients")
        self.assertEqual(events[0]['description'], "Client meeting")
        self.assertEqual(events[0]['date'], "2024-04-05")
        self.assertEqual(events[0]['time'], "15:00")

    def test_delete_event(self):
        add_event("Meeting", "Team meeting", "2024-04-03", "14:00")
        self.assertTrue(delete_event("Meeting"))
        self.assertEqual(len(events), 0)

if __name__ == "__main__":
    unittest.main()

