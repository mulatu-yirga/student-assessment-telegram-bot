# Student Assessment Telegram Bot

A Telegram bot that allows university students to check their assessment results and send messages to instructors.

## Features

- ✅ View assessment results by Student ID
- ✅ Send messages to instructor
- ✅ Automatic total calculation
- ✅ Query logging
- ✅ Error handling
- ✅ Secure student data access

## Assessment Fields

Each student record contains:
- **Student_ID**: Unique identifier
- **Name**: Student's full name
- **Mid**: Midterm exam score
- **Assignment1**: First assignment score
- **Assignment2**: Second assignment score
- **Quiz**: Quiz score
- **Final**: Final exam score
- **Total**: Automatically calculated (Mid + Assignment1 + Assignment2 + Quiz + Final)

## Bot Commands

### `/start`
Display welcome message and available commands

### `/view_result`
Check your assessment results by entering your Student ID

Example:
```
Student: /view_result
Bot: Please enter your Student ID
Student: ETS1234
Bot: [Displays complete assessment breakdown]
```

**Note:** When you use this command, your Telegram ID is automatically registered so the instructor can send you broadcast messages.

### `/message`
Send a message to the instructor

Example:
```
Student: /message
Bot: Please type your message to the instructor
Student: I have a question about my quiz mark.
Bot: Your message has been sent to the instructor successfully!
```

The instructor will receive:
- Your name
- Your Student ID
- Your Telegram ID (for direct replies)
- Your username
- Your message

### `/broadcast` (Instructor Only)
Send a message to all registered students

Example:
```
Instructor: /broadcast
Bot: You will send a message to X registered students. Please type your broadcast message:
Instructor: Class will be held online tomorrow via Zoom.
Bot: ✅ Broadcast Complete - Sent: X, Failed: 0
```

All students will receive:
```
📢 Message from Instructor

Class will be held online tomorrow via Zoom.

━━━━━━━━━━━━━━━━━━━━
This message was sent to all students
```

### `/help`
Show help information and usage instructions

## Installation & Setup

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed.

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install python-telegram-bot==20.7 pandas==2.1.4
```

### Step 3: Create Your Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 4: Get Instructor Telegram ID

To get the instructor's Telegram ID:
1. Search for `@userinfobot` on Telegram
2. Start the bot and it will show your Telegram ID
3. The instructor should do this to get their ID

### Step 5: Configure the Bot

Open `bot.py` and update these lines:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your bot token
INSTRUCTOR_TELEGRAM_ID = "YOUR_INSTRUCTOR_ID_HERE"  # Replace with instructor's ID
```

### Step 6: Prepare Student Data

Edit `students.csv` with your actual student data. Format:
```csv
student_id,name,mid,assignment1,assignment2,quiz,final
ETS1234,John Doe,18,9,10,8,45
```

## Running the Bot

### Windows:
```bash
python bot.py
```

### Linux/Mac:
```bash
python3 bot.py
```

You should see:
```
🤖 Starting Student Assessment Bot...
✓ Loaded 10 student records
✅ Bot is running! Press Ctrl+C to stop.
```

## Usage

1. Open Telegram and search for your bot (using the username you created)
2. Click "Start" or send `/start`
3. Use `/view_result` to check your results
4. Use `/message` to contact your instructor

## File Structure

```
.
├── bot.py                    # Main bot application
├── students.csv              # Student data file
├── student_registry.csv      # Auto-generated: Telegram ID to Student ID mapping
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── query_log.txt            # Auto-generated query log
```

## Security Notes

- ⚠️ Keep your bot token secret
- ⚠️ Don't share the `students.csv` file publicly
- ⚠️ Students can only view their own results by entering their ID
- ⚠️ The bot doesn't store passwords or sensitive authentication data

## Troubleshooting

### Bot doesn't respond
- Check if the bot token is correct
- Make sure the bot is running
- Verify your internet connection

### "Student ID not found" error
- Check if the Student ID is spelled correctly
- Verify the ID exists in `students.csv`
- Student IDs are case-insensitive

### Messages not reaching instructor
- Verify the instructor Telegram ID is correct
- Make sure the instructor has started a chat with the bot first

### CSV file errors
- Ensure `students.csv` is in the same directory as `bot.py`
- Check that the CSV format is correct (no missing columns)
- Make sure all numeric fields contain valid numbers

## Optional Improvements Implemented

✅ `/help` command with detailed instructions
✅ Formatted student results with emojis
✅ Student data privacy (ID-based access only)
✅ Query logging to `query_log.txt`
✅ Error handling for invalid IDs and network issues
✅ Student Telegram ID registration system
✅ `/broadcast` command for instructor announcements
✅ Instructor receives student's Telegram ID for direct replies

## Future Enhancements

- 🔄 Admin command to update marks
- 🔐 Student authentication system
- 📊 Grade statistics and class average
- 📧 Email notifications
- 🗄️ Database integration (SQLite/PostgreSQL)

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, contact your system administrator or instructor.
