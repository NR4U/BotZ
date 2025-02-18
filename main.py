import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# استخدام المتغير البيئي للتوكن
TOKEN = os.environ.get("BOT_TOKEN")

# قائمة معرفات المشرفين
ADMIN_IDS = [5222039643]  # غير هذه الأرقام إلى معرفات المشرفين الحقيقية

# قاموس يحتوي على الردود التلقائية
auto_replies = {
    "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته",
    "صباح الخير": "صباح النور",
    "مساء الخير": "مساء النور",
}

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

def start(update: Update, context: CallbackContext):
    if update.message.chat.type == 'private':
        if is_admin(update.message.from_user.id):
            update.message.reply_text("مرحباً بك أيها المشرف! أنا بوت الردود التلقائية.")
        else:
            update.message.reply_text("عذراً، هذا البوت يعمل في المجموعات فقط.")
    else:
        update.message.reply_text("مرحباً! أنا بوت الردود التلقائية.")

def add_reply(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    
    if not is_admin(user_id):
        update.message.reply_text("عذراً، هذا الأمر متاح للمشرفين فقط.")
        return

    try:
        text = update.message.text.replace("/add ", "")
        keyword, reply = text.split("|")
        keyword = keyword.strip()
        reply = reply.strip()
        
        auto_replies[keyword] = reply
        update.message.reply_text(f"تم إضافة الرد بنجاح:\nالكلمة: {keyword}\nالرد: {reply}")
    except:
        update.message.reply_text("الصيغة غير صحيحة. استخدم: /add الكلمة المفتاحية | الرد")

def remove_reply(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    
    if not is_admin(user_id):
        update.message.reply_text("عذراً، هذا الأمر متاح للمشرفين فقط.")
        return

    try:
        keyword = update.message.text.replace("/remove ", "").strip()
        if keyword in auto_replies:
            del auto_replies[keyword]
            update.message.reply_text(f"تم حذف الرد للكلمة: {keyword}")
        else:
            update.message.reply_text("الكلمة المفتاحية غير موجودة.")
    except:
        update.message.reply_text("الصيغة غير صحيحة. استخدم: /remove الكلمة المفتاحية")

def list_replies(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    
    if not is_admin(user_id):
        update.message.reply_text("عذراً، هذا الأمر متاح للمشرفين فقط.")
        return

    if auto_replies:
        reply_text = "قائمة الردود التلقائية:\n\n"
        for keyword, reply in auto_replies.items():
            reply_text += f"الكلمة: {keyword}\nالرد: {reply}\n\n"
        update.message.reply_text(reply_text)
    else:
        update.message.reply_text("لا توجد ردود تلقائية مضافة.")

def handle_message(update: Update, context: CallbackContext):
    if update.message.chat.type not in ['group', 'supergroup']:
        return

    if update.message.text:
        message_text = update.message.text
        
        for keyword, reply in auto_replies.items():
            if keyword.lower() in message_text.lower():
                update.message.reply_text(reply)
                break

def main():
    # Create updater
    updater = Updater(TOKEN)

    # Get dispatcher
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add_reply))
    dp.add_handler(CommandHandler("remove", remove_reply))
    dp.add_handler(CommandHandler("list", list_replies))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
