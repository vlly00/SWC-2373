import requests
import getpass

# Webex API base URL
WEBEX_API_BASE_URL = "https://api.ciscospark.com/v1"

# Helper function to test the connection
def test_connection(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(f"{WEBEX_API_BASE_URL}/people/me", headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Helper function to display user information
def display_user_info(token):
    user_data = test_connection(token)
    if user_data:
        print("User Information:")
        print(f"Display Name: {user_data['displayName']}")
        print(f"Nickname: {user_data['nickName']}")
        print(f"Emails: {', '.join(user_data['emails'])}")
    else:
        print("Unable to retrieve user information. Please check your token.")

# Helper function to list rooms
def list_rooms(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(f"{WEBEX_API_BASE_URL}/rooms", headers=headers)
        response.raise_for_status()
        rooms = response.json()["items"][:5]  # Limit to the first 5 rooms
        return rooms
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Helper function to create a room
def create_room(token, title):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "title": title
    }
    try:
        response = requests.post(f"{WEBEX_API_BASE_URL}/rooms", headers=headers, json=payload)
        response.raise_for_status()
        room_data = response.json()
        return room_data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Helper function to send a message to a room
def send_message_to_room(token, room_id, message):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "roomId": room_id,
        "text": message
    }
    try:
        response = requests.post(f"{WEBEX_API_BASE_URL}/messages", headers=headers, json=payload)
        response.raise_for_status()
        print("Message sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print("Failed to send the message. Please check your token and try again.")

# Main function
def main():
    webex_token = getpass.getpass("Enter your Webex API token: ")

    while True:
        print("\nMain Menu:")
        print("0. Test connection with Webex server")
        print("1. Display user information")
        print("2. Display list of rooms")
        print("3. Create a room")
        print("4. Send a message to a room")
        print("5. Exit")
        
        choice = input("Enter the option number: ")

        if choice == "0":
            result = test_connection(webex_token)
            if result:
                print("Connection successful! Acknowledgment: Webex server is reachable.")
            else:
                print("Connection failed. Please check your token.")

        elif choice == "1":
            display_user_info(webex_token)

        elif choice == "2":
            rooms = list_rooms(webex_token)
            if rooms:
                print("List of Rooms:")
                for index, room in enumerate(rooms, start=1):
                    print(f"Room {index}:")
                    print(f"Room ID: {room['id']}")
                    print(f"Room Title: {room['title']}")
                    print(f"Date Created: {room['created']}")
                    print(f"Last Activity: {room['lastActivity']}")
            else:
                print("Failed to retrieve the list of rooms. Please check your token.")

        elif choice == "3":
            room_title = input("Enter the title for the new room: ")
            new_room = create_room(webex_token, room_title)
            if new_room:
                print("Room created successfully:")
                print(f"Room ID: {new_room['id']}")
                print(f"Room Title: {new_room['title']}")
                print(f"Date Created: {new_room['created']}")
                print(f"Last Activity: {new_room['lastActivity']}")
            else:
                print("Failed to create a new room. Please check your token.")

        elif choice == "4":
            rooms = list_rooms(webex_token)
            if rooms:
                print("List of Rooms:")
                for index, room in enumerate(rooms, start=1):
                    print(f"{index}. {room['title']}")
                room_choice = input("Choose a room (enter the corresponding number): ")
                if room_choice.isdigit() and 1 <= int(room_choice) <= len(rooms):
                    selected_room = rooms[int(room_choice) - 1]
                    message = input("Enter the message to send to the room: ")
                    send_message_to_room(webex_token, selected_room['id'], message)
                else:
                    print("Invalid room choice. Please choose a valid room.")
            else:
                print("Failed to retrieve the list of rooms. Please check your token.")

        elif choice == "5":
            print("Exiting the Webex Troubleshooting Tool")
            break

        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    main()
