from plyer import notification
from sys import argv

# Title and message for the notification
title = "Reminder"
msg: str = argv[1]

# Display the notification
notification.notify(
    title=title,
    message=msg,
    app_name="My Notification App",
    timeout=5
) # type: ignore
