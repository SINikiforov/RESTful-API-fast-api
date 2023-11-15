import httpx
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.question import Question
from database.database import get_db

app = FastAPI()


class QuestionsData(BaseModel):
    questions_num: int


# Функция для апроса к публичному API и сохранения вопросов в базу данных
async def fetch_and_save_questions(db: Session, num_requested: int):
    try:
        async with httpx.AsyncClient() as client:
            api_url = f"https://jservice.io/api/random?count={num_requested}"
            response = await client.get(api_url)
            response.raise_for_status()
            quiz_data = response.json()

            for question in quiz_data:
                existing_question = db.query(Question).filter(Question.question_text == question["question"]).first()
                if existing_question:
                    continue

                db_question = Question(
                    question_text=question["question"],
                    answer_text=question["answer"]
                )
                db.add(db_question)
            db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error db {e}")


# Обработчик POST-запроса
@app.post("/get_questions/")
async def get_questions(questions_data: QuestionsData, db: Session = Depends(get_db)):
    if questions_data.questions_num <= 0:
        raise HTTPException(status_code=400, detail="Number of questions should be greater than 0")
    try:
        num_requested = questions_data.questions_num
        # Получаем предыдущий сохраненный вопрос
        prev_question = db.query(Question).order_by(Question.created_at.desc()).first()
        # Если вопросов нет в базе данных, пустой объект
        if prev_question:
            prev_question = {
                "id": prev_question.id,
                "question_text": prev_question.question_text,
                "answer_text": prev_question.answer_text,
                "created_at": prev_question.created_at,
            }
        else:
            prev_question = {}

        # Асинхронно получаем и сохраняем новые вопросы
        await fetch_and_save_questions(db, num_requested)

        return prev_question
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error {e}")

