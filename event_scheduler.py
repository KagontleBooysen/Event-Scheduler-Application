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
        print("Event added successfully.")
    else:
        print("Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time.")

# Function to display all events sorted by date and time
def display_events_sorted():
    if not events:
        print("No events found.")
    else:
        sorted_events = sorted(events, key=lambda x: (x['date'], x['time']))
        for event in sorted_events:
            print(f"Title: {event['title']}\nDescription: {event['description']}\nDate: {event['date']}\nTime: {event['time']}\n")

# Function to search events by date or keyword in title/description
def search_events(query):
    found_events = [event for event in events if query in event['title'] or query in event['description'] or query == event['date']]
    if found_events:
        for event in found_events:
            print(f"Title: {event['title']}\nDescription: {event['description']}\nDate: {event['date']}\nTime: {event['time']}\n")
    else:
        print("No matching events found.")

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
            print("Event edited successfully.")
            return
    print("Event not found.")

# Function to delete an event
def delete_event(title):
    global events
    updated_events = [event for event in events if event['title'] != title]
    if len(updated_events) < len(events):
        events = updated_events
        print("Event deleted successfully.")
    else:
        print("Event not found.")

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
            add_event(title, description, date, time)
        elif choice == '2':
            display_events_sorted()
        elif choice == '3':
            query = input("Enter search query (date or keyword): ")
            search_events(query)
        elif choice == '4':
            title = input("Enter title of event to edit: ")
            new_title = input("Enter new title (leave blank to keep current): ")
            new_description = input("Enter new description (leave blank to keep current): ")
            new_date = input("Enter new date (YYYY-MM-DD, leave blank to keep current): ")
            new_time = input("Enter new time (HH:MM, leave blank to keep current): ")
            edit_event(title, new_title, new_description, new_date, new_time)
        elif choice == '5':
            title = input("Enter title of event to delete: ")
            delete_event(title)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

