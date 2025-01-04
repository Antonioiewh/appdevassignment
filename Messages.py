import shelve
from datetime import datetime

class Message:
    def __init__(self, sender_id, receiver_id, content):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.timestamp = datetime.now()

    def to_dict(self):
        """Return a dictionary representation of the message."""
        return {
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M")
        }

class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def send_message(self, receiver_id, content, messages_db):
        message = Message(self.user_id, receiver_id, content)
        messages_list = messages_db.get("Messages", [])
        messages_list.append(message)
        messages_db["Messages"] = messages_list

        # Add to recent chats for both sender and receiver
        self.add_to_recent_chats(receiver_id)
        recipient = User(receiver_id)
        recipient.add_to_recent_chats(self.user_id)

    def add_to_recent_chats(self, receiver_id):
        # Ensure RecentChats structure exists
        with shelve.open("recentChat.db") as db:
            if str(self.user_id) not in db:
                db[str(self.user_id)] = []
                print("user id recent chats initialised")
            recent_chats = db[str(self.user_id)]
            print(f"Current recent chats for user {self.user_id}: {recent_chats}")
            if not any(chat['receiver_id'] == receiver_id for chat in recent_chats):
                recent_chats.append({"receiver_id": receiver_id})
            print(recent_chats)
            # Save updated recent chats back to the database
            db[str(self.user_id)] = recent_chats

    def get_received_messages(self, messages_db):
        """Retrieve all messages sent to this user."""
        if "Messages" not in messages_db:
            return []
        return [
            message.to_dict() for message in messages_db["Messages"]
            if message.receiver_id == self.user_id
        ]

    def get_sent_messages(self, messages_db):
        """Retrieve all messages sent by this user."""
        if "Messages" not in messages_db:
            return []
        return [
            message.to_dict() for message in messages_db["Messages"]
            if message.sender_id == self.user_id
        ]

    def get_recent_chats(self):
        """Get the list of recent chats for the current user."""
        with shelve.open("recentChat.db") as db:
            # Ensure the user_id exists and has a list of recent chats
            if str(self.user_id) in db:
                recent_chats = db[str(self.user_id)]
                if isinstance(recent_chats, list):
                    return recent_chats
