import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загрузка вопросов
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Сессии пользователей: user_id -> состояние
user_sessions = {}

# Загрузка и сохранение результатов
def load_results():
    try:
        with open("results.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_results(results):
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_sessions[update.effective_user.id] = {}
    await update.message.reply_text(
        "Привет! Выберите режим теста:",
        reply_markup=ReplyKeyboardMarkup([["Обучение", "Контроль"]], one_time_keyboard=True)
    )

async def mode_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = update.message.text.strip().lower()
    if mode not in ["обучение", "контроль"]:
        await update.message.reply_text("Пожалуйста, выберите режим: Обучение или Контроль.")
        return
    user_id = update.effective_user.id
    user_sessions[user_id] = {
        "mode": mode,
        "current": 0,
        "score": 0,
        "answers": []
    }
    await send_question(update, context, user_id)

async def send_question(update, context, user_id):
    session = user_sessions[user_id]
    idx = session["current"]
    if idx >= len(questions):
        await finish_test(update, context, user_id)
        return
    q = questions[idx]
    reply_markup = ReplyKeyboardMarkup([[opt] for opt in q["options"]], one_time_keyboard=True)
    await update.message.reply_text(f"Вопрос {idx + 1}/{len(questions)}:\n{q['question']}", reply_markup=reply_markup)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_sessions or "mode" not in user_sessions[user_id]:
        await update.message.reply_text("Сначала выберите режим теста: /start")
        return
    session = user_sessions[user_id]
    idx = session["current"]
    q = questions[idx]
    user_answer = update.message.text
    try:
        user_choice = q["options"].index(user_answer)
    except ValueError:
        await update.message.reply_text("Пожалуйста, выберите один из предложенных вариантов.")
        return

    is_correct = (user_choice == q["correct_option"])
    session["answers"].append({"question_id": q["id"], "answer": user_choice, "correct": is_correct})
    if is_correct:
        session["score"] += 1

    # В режиме обучения сразу выводим пояснение
    if session["mode"] == "обучение":
        explanation = q["explanation"] if not is_correct else "Верно!"
        await update.message.reply_text(explanation)

    session["current"] += 1
    if session["current"] < len(questions):
        await send_question(update, context, user_id)
    else:
        await finish_test(update, context, user_id)

async def finish_test(update, context, user_id):
    session = user_sessions[user_id]
    total = len(questions)
    score = session["score"]
    result_text = f"Тест завершён!\nВаш результат: {score} из {total}."
    await update.message.reply_text(result_text)
    # В режиме контроль выводим пояснения только сейчас
    if session["mode"] == "контроль":
        for i, ans in enumerate(session["answers"]):
            q = questions[i]
            if not ans["correct"]:
                await update.message.reply_text(
                    f"Вопрос: {q['question']}\nВаш ответ: {q['options'][ans['answer']]}\nПравильный ответ: {q['options'][q['correct_option']]}\nПояснение: {q['explanation']}"
                )
    # Сохраняем результат
    results = load_results()
    results.append({
        "user_id": user_id,
        "username": update.effective_user.username,
        "score": score,
        "total": total,
        "mode": session["mode"],
        "answers": session["answers"]
    })
    save_results(results)
    # Сброс сессии
    del user_sessions[user_id]

def main():
    app = Application.builder().token("7569213821:AAGkCNqk8Bf74TNwCkxHCBWaTTWmDlUfqzA").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("^(Обучение|Контроль)$"), mode_choice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))
    app.run_polling()

if __name__ == "__main__":
    main()
