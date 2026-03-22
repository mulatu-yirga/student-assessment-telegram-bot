"""
Telegram Bot for Student Assessment Results
This bot allows students to check their assessment results and send messages to instructors.
"""

import os
import pandas as pd
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

# Conversation states
WAITING_FOR_STUDENT_ID = 1
WAITING_FOR_MESSAGE = 2
WAITING_FOR_BROADCAST = 3

# Configuration
# Configuration - reads from environment variables (set via fly secrets)
BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT YOUR_TELEGRAM_BOT_TOKEN")
INSTRUCTOR_TELEGRAM_ID = os.getenv("INSTRUCTOR_TELEGRAM_ID", "PUT_YOUR_TELEGRAM_ID")
CSV_FILE = "students.csv"
STUDENT_REGISTRY_FILE = "student_registry.csv"

# Store student data globally
students_df = None
student_registry = {}  # Maps telegram_id to student info


def load_student_data():
    """Load student data from CSV file"""
    global students_df
    try:
        students_df = pd.read_csv(CSV_FILE)
        # Calculate total for each student
        students_df['total'] = (
            students_df['mid'] + 
            students_df['assignment1'] + 
            students_df['assignment2'] + 
            students_df['quiz'] + 
            students_df['final']
        )
        print(f"✓ Loaded {len(students_df)} student records")
        return True
    except FileNotFoundError:
        print(f"✗ Error: {CSV_FILE} not found!")
        return False
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False


def load_student_registry():
    """Load student registry (telegram_id to student_id mapping)"""
    global student_registry
    try:
        registry_df = pd.read_csv(STUDENT_REGISTRY_FILE)
        student_registry = registry_df.set_index('telegram_id').to_dict('index')
        print(f"✓ Loaded {len(student_registry)} registered students")
    except FileNotFoundError:
        print("ℹ No student registry found, creating new one")
        student_registry = {}
    except Exception as e:
        print(f"⚠ Error loading registry: {e}")
        student_registry = {}


def save_student_registry():
    """Save student registry to CSV"""
    try:
        registry_data = []
        for telegram_id, info in student_registry.items():
            registry_data.append({
                'telegram_id': telegram_id,
                'student_id': info['student_id'],
                'name': info['name']
            })
        registry_df = pd.DataFrame(registry_data)
        registry_df.to_csv(STUDENT_REGISTRY_FILE, index=False)
    except Exception as e:
        print(f"⚠ Error saving registry: {e}")


def register_student(telegram_id, student_id, name):
    """Register a student's Telegram ID"""
    student_registry[telegram_id] = {
        'student_id': student_id,
        'name': name
    }
    save_student_registry()


def escape_markdown(text):
    """Escape special Markdown characters"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, '\\' + char)
    return text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = (
        "🎓 *Welcome to the Student Assessment Bot!*\n\n"
        "📋 Available commands:\n"
        "/view\\_result – View your assessment results\n"
        "/message – Send a message to the instructor\n"
        "/help – Show help information\n\n"
        "Use any command to get started!"
    )
    await update.message.reply_text(welcome_message, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = (
        "📚 *Student Assessment Bot Help*\n\n"
        "*Commands:*\n"
        "• /start – Show welcome message\n"
        "• /view\\_result – Check your assessment results\n"
        "• /message – Send a message to your instructor\n"
        "• /help – Show this help message\n\n"
        "*How to use:*\n"
        "1️⃣ Use /view\\_result and enter your Student ID\n"
        "2️⃣ Use /message to contact your instructor\n\n"
        "⚠️ Keep your Student ID confidential!"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def view_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the view result conversation"""
    await update.message.reply_text(
        "🔍 Please enter your Student ID:\n"
        "(Example: WOUR/000/00)"
    )
    return WAITING_FOR_STUDENT_ID


async def process_student_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process the student ID and display results"""
    student_id = update.message.text.strip().upper()
    telegram_id = update.effective_user.id
    
    # Search for student in dataframe
    student = students_df[students_df['student_id'].str.upper() == student_id]
    
    if student.empty:
        await update.message.reply_text(
            "❌ Student ID not found. Please check and try again.\n\n"
            "Use /view_result to try again."
        )
        return ConversationHandler.END
    
    # Get student data
    student_data = student.iloc[0]
    
    # Register student's Telegram ID
    register_student(telegram_id, student_data['student_id'], student_data['name'])
    
    # Format result message
    result_message = (
        f"📊 *Student Assessment Result*\n\n"
        f"👤 *Name:* {student_data['name']}\n"
        f"🆔 *Student ID:* {student_data['student_id']}\n\n"
        f"📝 *Assessment Breakdown:*\n"
        f"• Mid: {student_data['mid']}\n"
        f"• Assignment 1: {student_data['assignment1']}\n"
        f"• Assignment 2: {student_data['assignment2']}\n"
        f"• Quiz: {student_data['quiz']}\n"
        f"• Final: {student_data['final']}\n\n"
        f"✅ *Total: {student_data['total']}*"
    )
    
    # Store student info for potential message sending
    context.user_data['student_id'] = student_data['student_id']
    context.user_data['student_name'] = student_data['name']
    context.user_data['telegram_id'] = telegram_id
    
    await update.message.reply_text(result_message, parse_mode='Markdown')
    
    # Log the query
    log_query(student_data['student_id'], student_data['name'], telegram_id)
    
    return ConversationHandler.END


async def message_instructor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the message conversation"""
    await update.message.reply_text(
        "✉️ Please type your message to the instructor:\n\n"
        "(Send /cancel to cancel)"
    )
    return WAITING_FOR_MESSAGE


async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process and forward the message to instructor"""
    student_message = update.message.text
    telegram_id = update.effective_user.id
    telegram_username = update.effective_user.username or "No username"
    
    # Get student info if available
    student_id = context.user_data.get('student_id', 'Unknown')
    student_name = context.user_data.get('student_name', 'Unknown')
    
    # Format message for instructor with Telegram ID (using plain text to avoid parsing errors)
    instructor_notification = (
        f"📬 NEW MESSAGE FROM STUDENT\n\n"
        f"👤 Name: {student_name}\n"
        f"🆔 Student ID: {student_id}\n"
        f"📱 Telegram ID: {telegram_id}\n"
        f"👥 Username: @{telegram_username}\n\n"
        f"💬 Message:\n{student_message}"
    )
    
    try:
        # Send message to instructor (no Markdown parsing)
        await context.bot.send_message(
            chat_id=INSTRUCTOR_TELEGRAM_ID,
            text=instructor_notification
        )
        
        await update.message.reply_text(
            "✅ Your message has been sent to the instructor successfully!"
        )
    except Exception as e:
        await update.message.reply_text(
            "❌ Failed to send message. Please try again later."
        )
        print(f"Error sending message to instructor: {e}")
    
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current conversation"""
    await update.message.reply_text(
        "❌ Operation cancelled.\n\n"
        "Use /start to see available commands."
    )
    return ConversationHandler.END


def log_query(student_id, student_name, telegram_id=None):
    """Log student queries to a file"""
    try:
        from datetime import datetime
        with open('query_log.txt', 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tg_info = f" (TG: {telegram_id})" if telegram_id else ""
            f.write(f"{timestamp} - {student_id} ({student_name}){tg_info} viewed results\n")
    except Exception as e:
        print(f"Error logging query: {e}")


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start broadcast message (instructor only)"""
    user_id = str(update.effective_user.id)
    
    # Check if user is instructor
    if user_id != INSTRUCTOR_TELEGRAM_ID:
        await update.message.reply_text("❌ This command is only available to instructors.")
        return ConversationHandler.END
    
    if not student_registry:
        await update.message.reply_text(
            "⚠️ No students registered yet.\n"
            "Students need to use /view_result first to register."
        )
        return ConversationHandler.END
    
    await update.message.reply_text(
        f"📢 *Broadcast Message*\n\n"
        f"You will send a message to *{len(student_registry)} registered students*.\n\n"
        f"Please type your broadcast message:\n\n"
        f"(Send /cancel to cancel)",
        parse_mode='Markdown'
    )
    return WAITING_FOR_BROADCAST


async def process_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process and send broadcast message to all students"""
    broadcast_message = update.message.text
    
    success_count = 0
    fail_count = 0
    
    # Send to all registered students (using plain text to avoid parsing errors)
    for telegram_id, info in student_registry.items():
        try:
            message = (
                f"📢 MESSAGE FROM INSTRUCTOR\n\n"
                f"{broadcast_message}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"This message was sent to all students"
            )
            await context.bot.send_message(
                chat_id=telegram_id,
                text=message
            )
            success_count += 1
        except Exception as e:
            fail_count += 1
            print(f"Failed to send to {telegram_id} ({info['name']}): {e}")
    
    # Send summary to instructor
    summary = (
        f"✅ BROADCAST COMPLETE\n\n"
        f"📤 Sent: {success_count}\n"
        f"❌ Failed: {fail_count}\n"
        f"📊 Total: {len(student_registry)}"
    )
    await update.message.reply_text(summary)
    
    return ConversationHandler.END


def main():
    """Main function to run the bot"""
    print("🤖 Starting Student Assessment Bot...")
    
    # Load student data
    if not load_student_data():
        print("❌ Cannot start bot without student data!")
        return
    
    # Load student registry
    load_student_registry()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Set bot commands menu (appears at bottom left)
    async def post_init(app: Application):
        # Commands for all users
        await app.bot.set_my_commands([
            BotCommand("start", "Welcome to the Student Assessment Bot"),
            BotCommand("view_result", "View your assessment result"),
            BotCommand("message", "Send a message to the instructor"),
            BotCommand("help", "Show information")
        ])
    
    application.post_init = post_init
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Conversation handler for viewing results
    view_result_handler = ConversationHandler(
        entry_points=[CommandHandler("view_result", view_result)],
        states={
            WAITING_FOR_STUDENT_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_student_id)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(view_result_handler)
    
    # Conversation handler for messaging instructor
    message_handler = ConversationHandler(
        entry_points=[CommandHandler("message", message_instructor)],
        states={
            WAITING_FOR_MESSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_message)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(message_handler)
    
    # Conversation handler for broadcast (instructor only)
    broadcast_handler = ConversationHandler(
        entry_points=[CommandHandler("broadcast", broadcast)],
        states={
            WAITING_FOR_BROADCAST: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_broadcast)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(broadcast_handler)
    
    # Start the bot
    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
