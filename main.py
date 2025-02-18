import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

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

# دالة للتحقق من صلاحيات المشرف
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == 'private':
        if is_admin(update.message.from_user.id):
            await update.message.reply_text("مرحباً بك أيها المشرف! أنا بوت الردود التلقائية.")
        else:
            await update.message.reply_text("عذراً، هذا البوت يعمل في المجموعات فقط.")
    else:
        await update.message.reply_text("مرحباً! أنا بوت الردود التلقائية.")

async def add_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("عذراً، هذا الأمر متاح للمشرفين فقط.")
        return

    try:
        text = update.message.text.replace("/add ", "")
        keyword, reply = text.split("|")
        keyword = keyword.strip()
        reply = reply.strip()
        
        auto_replies[keyword] = reply
        await update.message.reply_text(f"تم إضافة الرد بنجاح:\nالكلمة: {keyword}\nالرد: {reply}")
    except:
        await update.message.reply_text("الصيغة غير صحيحة. استخدم: /add الكلمة المفتاحية | الرد")

async def remove_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("عذراً، هذا الأمر متاح للمشرفين فقط.")
        return

    try:
        keyword = update.message.text.replace("/remove ", "").strip()
        if keyword in auto_replies:
            del auto_replies[keyword]
            await update.message.reply_text(f"تم حذف الرد للكلمة: {keyword}")
        else:
            await update.message.reply_text("الكلمة المفتاحية غير موجودة.")
    except:
        await update.message.reply_text("الصيغة غير صحيحة. استخدم: /remove الكلمة المفتاحية")

async def list_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("عذراً، هذا الأمر متاح للمشرفين فقط.")
        return

    if auto_replies:
        reply_text = "قائمة الردود التلقائية:\n\n"
        for keyword, reply in auto_replies.items():
            reply_text += f"الكلمة: {keyword}\nالرد: {reply}\n\n"
        await update.message.reply_text(reply_text)
    else:
        await update.message.reply_text("لا توجد ردود تلقائية مضافة.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type not in ['group', 'supergroup']:
        return

    if update.message.text:
        message_text = update.message.text
        
        for keyword, reply in auto_replies.items():
            if keyword.lower() in message_text.lower():
                await update.message.reply_text(reply)
                break

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_reply))
    application.add_handler(CommandHandler("remove", remove_reply))
    application.add_handler(CommandHandler("list", list_replies))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
