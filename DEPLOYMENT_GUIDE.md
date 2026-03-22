# Telegram Bot Deployment Guide

This guide covers multiple ways to deploy your Student Assessment Telegram Bot so it runs 24/7.

## 🎯 Deployment Options

1. **PythonAnywhere** (Free, Easiest for beginners)
2. **Heroku** (Free tier available, Popular)
3. **Railway** (Modern, Easy to use)
4. **VPS/Cloud Server** (DigitalOcean, AWS, Google Cloud)
5. **Local Computer** (For testing only)

---

## 1. 🐍 PythonAnywhere (Recommended for Beginners)

### Pros:
- Free tier available
- No credit card required
- Easy to set up
- Good for learning

### Steps:

1. **Create Account**
   - Go to https://www.pythonanywhere.com
   - Sign up for a free account

2. **Upload Files**
   - Go to "Files" tab
   - Create a new directory: `student_bot`
   - Upload: `bot.py`, `students.csv`, `requirements.txt`

3. **Install Dependencies**
   - Go to "Consoles" tab
   - Start a Bash console
   ```bash
   cd student_bot
   pip3.10 install --user -r requirements.txt
   ```

4. **Run the Bot**
   - In the console:
   ```bash
   python3.10 bot.py
   ```

5. **Keep it Running (Always On)**
   - Go to "Tasks" tab
   - Add a new "Always-on task"
   - Command: `python3.10 /home/yourusername/student_bot/bot.py`

### Note:
Free accounts have limitations. For 24/7 operation, consider upgrading to a paid plan ($5/month).

---

## 2. 🚀 Heroku Deployment

### Pros:
- Free tier available (with credit card)
- Automatic deployment from Git
- Easy scaling

### Steps:

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Required Files**

   Create `Procfile` (no extension):
   ```
   worker: python bot.py
   ```

   Create `runtime.txt`:
   ```
   python-3.11.0
   ```

3. **Initialize Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

4. **Create Heroku App**
   ```bash
   heroku login
   heroku create your-student-bot
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set BOT_TOKEN="your_bot_token_here"
   heroku config:set INSTRUCTOR_ID="instructor_telegram_id"
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

7. **Scale Worker**
   ```bash
   heroku ps:scale worker=1
   ```

8. **View Logs**
   ```bash
   heroku logs --tail
   ```

---

## 3. 🚂 Railway Deployment

### Pros:
- Modern interface
- Free $5 credit monthly
- Easy GitHub integration

### Steps:

1. **Create Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository

3. **Add Environment Variables**
   - Go to "Variables" tab
   - Add:
     - `BOT_TOKEN`: your bot token
     - `INSTRUCTOR_ID`: instructor's Telegram ID

4. **Configure Start Command**
   - Railway auto-detects Python
   - Or manually set: `python bot.py`

5. **Deploy**
   - Railway automatically deploys on push

---

## 4. 🖥️ VPS/Cloud Server (DigitalOcean, AWS, etc.)

### Pros:
- Full control
- Can run multiple bots
- Best for production

### Steps (Ubuntu/Debian):

1. **Create Server**
   - Create a droplet/instance (Ubuntu 22.04)
   - Connect via SSH

2. **Update System**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

3. **Install Python & Dependencies**
   ```bash
   sudo apt install python3 python3-pip -y
   ```

4. **Upload Files**
   ```bash
   # Use SCP or SFTP
   scp -r * user@your-server-ip:/home/user/student_bot/
   ```

5. **Install Requirements**
   ```bash
   cd student_bot
   pip3 install -r requirements.txt
   ```

6. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/student-bot.service
   ```

   Add:
   ```ini
   [Unit]
   Description=Student Assessment Telegram Bot
   After=network.target

   [Service]
   Type=simple
   User=your-username
   WorkingDirectory=/home/your-username/student_bot
   ExecStart=/usr/bin/python3 /home/your-username/student_bot/bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

7. **Enable and Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable student-bot
   sudo systemctl start student-bot
   ```

8. **Check Status**
   ```bash
   sudo systemctl status student-bot
   ```

9. **View Logs**
   ```bash
   sudo journalctl -u student-bot -f
   ```

---

## 5. 💻 Local Computer (Testing Only)

### Windows:

1. **Keep Terminal Open**
   ```bash
   python bot.py
   ```

2. **Run in Background (PowerShell)**
   ```powershell
   Start-Process python -ArgumentList "bot.py" -WindowStyle Hidden
   ```

3. **Create Batch File** (`start_bot.bat`):
   ```batch
   @echo off
   python bot.py
   pause
   ```

### Linux/Mac:

1. **Run in Background**
   ```bash
   nohup python3 bot.py > bot.log 2>&1 &
   ```

2. **Check if Running**
   ```bash
   ps aux | grep bot.py
   ```

3. **Stop Bot**
   ```bash
   pkill -f bot.py
   ```

---

## 🔒 Security Best Practices

### 1. Use Environment Variables

Modify `bot.py` to use environment variables:

```python
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
INSTRUCTOR_TELEGRAM_ID = os.getenv("INSTRUCTOR_ID", "YOUR_INSTRUCTOR_ID_HERE")
```

### 2. Never Commit Secrets

Add to `.gitignore`:
```
bot_token.txt
config.py
.env
```

### 3. Use .env File (Optional)

Install python-dotenv:
```bash
pip install python-dotenv
```

Create `.env`:
```
BOT_TOKEN=your_token_here
INSTRUCTOR_ID=your_id_here
```

Update `bot.py`:
```python
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
INSTRUCTOR_TELEGRAM_ID = os.getenv("INSTRUCTOR_ID")
```

---

## 📊 Monitoring Your Bot

### Check if Bot is Running:

1. **Send /start to your bot**
2. **Check logs** (depends on hosting platform)
3. **Use monitoring tools**:
   - UptimeRobot (https://uptimerobot.com)
   - Healthchecks.io (https://healthchecks.io)

### Common Issues:

**Bot not responding:**
- Check if process is running
- Verify bot token is correct
- Check internet connection
- Review error logs

**Bot stops after some time:**
- Use process manager (systemd, PM2)
- Enable auto-restart
- Check for memory issues

---

## 🎓 Recommended Deployment Path

### For Learning/Testing:
1. Start with **Local Computer**
2. Move to **PythonAnywhere** (free)

### For Production:
1. Use **Railway** or **Heroku** (easy)
2. Or **VPS** (full control)

---

## 📝 Deployment Checklist

Before deploying:

- [ ] Bot token is configured
- [ ] Instructor Telegram ID is set
- [ ] `students.csv` is uploaded
- [ ] Dependencies are installed
- [ ] Bot responds to /start command
- [ ] Secrets are not in Git repository
- [ ] Auto-restart is configured
- [ ] Logs are accessible
- [ ] Backup of student data exists

---

## 🆘 Troubleshooting

### "Bot not responding"
```bash
# Check if bot is running
ps aux | grep bot.py

# Check logs
tail -f bot.log

# Restart bot
sudo systemctl restart student-bot
```

### "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### "Permission denied"
```bash
# Fix file permissions
chmod +x bot.py
```

---

## 📞 Support

For deployment issues:
- Check platform documentation
- Review error logs
- Test locally first
- Verify all credentials

## 🔗 Useful Links

- PythonAnywhere: https://www.pythonanywhere.com
- Heroku: https://www.heroku.com
- Railway: https://railway.app
- DigitalOcean: https://www.digitalocean.com
- Telegram Bot API: https://core.telegram.org/bots/api
