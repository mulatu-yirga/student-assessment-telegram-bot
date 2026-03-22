# Quick Setup Guide

## 🚀 Getting Started in 5 Minutes

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Your Telegram Bot

1. Open Telegram
2. Search for `@BotFather`
3. Send: `/newbot`
4. Choose a name: `Student Assessment Bot`
5. Choose a username: `your_university_assessment_bot`
6. **Copy the token** (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. Get Instructor Telegram ID

1. Instructor opens Telegram
2. Search for `@userinfobot`
3. Start the bot
4. **Copy the ID number** (looks like: `123456789`)

### 4. Configure bot.py

Open `bot.py` and replace:

```python
BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # Your actual token
INSTRUCTOR_TELEGRAM_ID = "123456789"  # Instructor's actual ID
```

### 5. Add Your Student Data

Edit `students.csv` with real student information:

```csv
student_id,name,mid,assignment1,assignment2,quiz,final
ETS1234,John Doe,18,9,10,8,45
ETS1235,Jane Smith,20,10,9,9,48
```

### 6. Run the Bot

```bash
python bot.py
```

You should see:
```
🤖 Starting Student Assessment Bot...
✓ Loaded X student records
✅ Bot is running! Press Ctrl+C to stop.
```

### 7. Test the Bot

1. Open Telegram
2. Search for your bot username
3. Click "Start"
4. Try: `/view_result`
5. Enter a Student ID from your CSV

## 📝 Example Interaction

```
You: /start
Bot: 🎓 Welcome to the Student Assessment Bot!
     Available commands:
     /view_result – View your assessment results
     /message – Send a message to the instructor
     /help – Show help information

You: /view_result
Bot: 🔍 Please enter your Student ID:

You: ETS1234
Bot: 📊 Student Assessment Result
     
     👤 Name: John Doe
     🆔 Student ID: ETS1234
     
     📝 Assessment Breakdown:
     • Mid: 18
     • Assignment 1: 9
     • Assignment 2: 10
     • Quiz: 8
     • Final: 45
     
     ✅ Total: 90
```

## ⚠️ Common Issues

### "ModuleNotFoundError: No module named 'telegram'"
**Solution:** Run `pip install python-telegram-bot`

### "FileNotFoundError: students.csv"
**Solution:** Make sure `students.csv` is in the same folder as `bot.py`

### Bot doesn't respond
**Solution:** 
- Check if bot token is correct
- Make sure bot is running (`python bot.py`)
- Verify internet connection

### "Unauthorized" error
**Solution:** Double-check your bot token from @BotFather

## 🎯 Next Steps

- Add more students to `students.csv`
- Test the `/message` command
- Check `query_log.txt` to see student queries
- Share bot username with students

## 📞 Need Help?

Refer to the full `README.md` for detailed documentation.
