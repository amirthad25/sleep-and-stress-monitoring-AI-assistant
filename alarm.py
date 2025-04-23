import time
from datetime import datetime
import pygame
import os
from plyer import notification
from twilio.rest import Client

# Twilio Credentials (Replace with your actual credentials)
TWILIO_SID = "ACcbb156d81cb7c87e50ccf9101939809f"
TWILIO_AUTH_TOKEN = "978d7bc167e57d28f0e94a052dc804fc"
TWILIO_PHONE_NUMBER = "+19202899277"
USER_PHONE_NUMBER = "+916369311554"

# Get user-defined alarm time
alarm_time = input("Enter the time for sleep reminder (HH:MM, 24-hour format): ").strip()

# Validate user input
if not alarm_time or len(alarm_time) != 5 or alarm_time[2] != ":":
    print("❌ Invalid time format! Please enter in HH:MM (24-hour format).")
    exit()

# Alarm sound file
ALARM_SOUND = "alarm.wav"

def send_sms():
    """Send SMS alert using Twilio"""
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"🔔 Reminder: It's {alarm_time}! Time to sleep! 🔔",
            from_=TWILIO_PHONE_NUMBER,
            to=USER_PHONE_NUMBER
        )
        print(f"📩 SMS Sent! Message SID: {message.sid}")
    except Exception as e:
        print(f"⚠️ SMS sending failed: {e}")

def play_alarm():
    """Trigger alarm sound, notification, and SMS"""
    print(f"🔔 Time to sleep! It's {alarm_time}! 🔔")

    # Show Desktop Notification
    try:
        notification.notify(
            title="Sleep Reminder",
            message=f"🔔 Time to sleep! It's {alarm_time}!",
            timeout=10
        )
    except Exception as e:
        print(f"⚠️ Notification error: {e}")

    # Play alarm sound if file exists
    if os.path.exists(ALARM_SOUND):
        try:
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(ALARM_SOUND)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                time.sleep(1)  # Wait for sound to finish
        except Exception as e:
            print(f"⚠️ Pygame sound error: {e}")
    else:
        print("⚠️ Alarm sound file not found! Please check 'alarm.wav'.")

    # Send SMS Alert
    send_sms()

print(f"⏳ Alarm set for {alarm_time}. Script is running...")

while True:
    now = datetime.now().strftime("%H:%M")  # Get current time in HH:MM format
    print(f"⌛ Checking time... Current time: {now}")

    if now == alarm_time:
        play_alarm()
        break  # Stop execution after playing alarm
    time.sleep(10)  # Check every 10 seconds
