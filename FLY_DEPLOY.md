# Deploy to Fly.io (Free 24/7)

## Step 1: Install flyctl

Download and install the Fly.io CLI:

Windows (PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://fly.io/install.ps1 | iex"
```

## Step 2: Sign Up & Login

```bash
flyctl auth signup
```
Or if you already have an account:
```bash
flyctl auth login
```

## Step 3: Launch the App

Run this inside your project folder:
```bash
flyctl launch  //to run the app
```

When prompted:
- App name: student-assessment-bot (or any unique name)
- Region: choose closest to you
- Would you like to set up a Postgresql database? → No
- Would you like to deploy now? → No (we set secrets first)

## Step 4: Set Secret Environment Variables

```bash
flyctl secrets set BOT_TOKEN="your_bot_token_here"
flyctl secrets set INSTRUCTOR_TELEGRAM_ID="your_instructor_telegram_id"
```

## Step 5: Deploy

```bash
flyctl deploy
```

## Step 6: Verify it's Running

```bash
flyctl status
flyctl logs
```

You should see:
```
✓ Loaded 10 student records
✅ Bot is running!
```

---

## Useful Commands

| Command | Description |
|---|---|
| `flyctl status` | Check if app is running |
| `flyctl logs` | View live logs |
| `flyctl deploy` | Redeploy after changes |
| `flyctl secrets list` | List set secrets |
| `flyctl suspend` | Pause the app |
| `flyctl resume` | Resume the app |

---

## Updating Student Data

Since students.csv is baked into the Docker image, after editing it you need to redeploy:

```bash
flyctl deploy
```

---

## Free Plan Limits

Fly.io free tier includes:
- 3 shared-cpu-1x VMs with 256MB RAM
- Enough to run this bot 24/7 for free
- No credit card required for free tier apps
