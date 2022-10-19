Terminal:uvicorn main:app --reload
docker-compose up --build
alembic revision --autogenerate -m "<title>"
alembic upgrade head
  
