from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio
import json

# File to store the wish list
WISH_LIST_FILE = "wish_list.json"


# Load the wish list from the file
def load_wish_list():
    try:
        with open(WISH_LIST_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Save the wish list to the file
def save_wish_list():
    with open(WISH_LIST_FILE, "w") as file:
        json.dump(wish_list, file)


# Initialize the wish list
wish_list = load_wish_list()


async def show_options(update: Update) -> None:
    """Show available options to the user."""
    await update.message.reply_text(
        "Here are the commands you can use:\n" \
        "/add - Add a new wish\n" \
        "/list - Show the wish list\n" \
        "/delete - Delete a wish from the list\n"
    )


async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! I am your Wish List Bot.\n\n"
    )
    await show_options(update)


async def add_wish(update: Update, context: CallbackContext) -> None:
    """Prompt the user to add a wish."""
    await update.message.reply_text(
        "What is your wish? Please type it below."
    )

    # Save the next message handler for adding the wish
    context.user_data['waiting_for_wish'] = True


async def list_wishes(update: Update, context: CallbackContext) -> None:
    """Show all the wishes in the list."""
    if not wish_list:
        await update.message.reply_text("Your wish list is empty!")
    else:
        wishes = "\n".join(f"{i + 1}. {wish}" for i, wish in enumerate(wish_list))
        await update.message.reply_text(f"Here are your wishes:\n{wishes}")
    await show_options(update)


async def delete_wish(update: Update, context: CallbackContext) -> None:
    """Prompt the user to delete a wish by its number."""
    if not wish_list:
        await update.message.reply_text("Your wish list is empty! Nothing to delete.")
        await show_options(update)
    else:
        wishes = "\n".join(f"{i + 1}. {wish}" for i, wish in enumerate(wish_list))
        await update.message.reply_text(
            f"Here are your wishes:\n{wishes}\n\n" \
            "Please type the number of the wish you want to delete."
        )
        context.user_data['waiting_for_delete'] = True


async def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle incoming messages."""
    # Check if we are waiting for a wish
    if context.user_data.get('waiting_for_wish'):
        wish = update.message.text
        wish_list.append(wish)
        save_wish_list()  # Save the updated list
        await update.message.reply_text(f"Added your wish: '{wish}'")

        # Clear the waiting state
        context.user_data['waiting_for_wish'] = False
        await show_options(update)
    elif context.user_data.get('waiting_for_delete'):
        try:
            index = int(update.message.text) - 1
            if 0 <= index < len(wish_list):
                deleted_wish = wish_list.pop(index)
                save_wish_list()  # Save after deletion
                await update.message.reply_text(f"Deleted your wish: '{deleted_wish}'")
            else:
                await update.message.reply_text("Invalid number. Please try again.")
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")

        # Clear the waiting state
        context.user_data['waiting_for_delete'] = False
        await show_options(update)
    else:
        await update.message.reply_text(
            "I didn't understand that. Please use /add to add a wish, /list to see your wish list, or /delete to remove a wish."
        )
        await show_options(update)


def main():
    """Run the bot."""
    token = "********************************"
    application = Application.builder().token(token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_wish))
    application.add_handler(CommandHandler("list", list_wishes))
    application.add_handler(CommandHandler("delete", delete_wish))

    # Register a message handler for adding and deleting wishes
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    application.run_polling()


if __name__ == '__main__':
    main()
