import shelve
from datetime import datetime
import uuid

class Message:
    def __init__(self, sender_id, receiver_id, content, type, uuid, extension, listing_id, reply_value, replier_id):
        self.sender_id = int(sender_id)
        self.receiver_id = int(receiver_id)
        self.content = content
        self.timestamp = datetime.now()
        self.message_id = uuid
        self.status = "active"  # status of message: "active" or "deleted" or "edited"
        self.type = type # text or picture or text+pic
        self.extension = extension
        self.listing_id = listing_id
        self.reply_value = reply_value
        self.replier_id = replier_id
    def to_dict(self):
        """Return a dictionary representation of the message."""
        return {
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M"),
            "message_id": self.message_id,
            "type": self.type
        }

class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def send_message(self, receiver_id, content, messages_db, message_type, UUID, extension, listing_id, reply_value, replier_id):
        content = content.strip()
        message = Message(self.user_id, receiver_id, content, message_type, UUID, extension, listing_id, reply_value, replier_id)

        # add message to database
        messages_list = messages_db.get("Messages", [])
        messages_list.append(message)
        messages_db["Messages"] = messages_list

        self.add_to_recent_chats(receiver_id)  # Updates recent chats list for the sender, moves it to top
        recipient = User(receiver_id)
        recipient.add_to_recent_chats(self.user_id)  # Updates recent chats list for the receiver

    def add_to_recent_chats(self, receiver_id):
        # Ensure RecentChats structure exists
        with shelve.open("recentChat.db") as db:
            user_chats_key = str(self.user_id)

            if user_chats_key not in db:
                db[user_chats_key] = []

            # retrieve and update the list of recent chats
            recent_chats = db[user_chats_key]

            # remove receiver_id if it exists to avoid dupes
            recent_chats = [chat for chat in recent_chats if chat['receiver_id'] != receiver_id]

            # add receiver to the top of the list
            recent_chats.insert(0, {"receiver_id": receiver_id})

            # save updated recent chats back to database
            db[user_chats_key] = recent_chats

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