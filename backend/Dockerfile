FROM python:3.7-slim
WORKDIR /app
COPY ./backend/requirements.txt .
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY ./backend .
RUN pip install psycopg2-binary
CMD ["gunicorn", "foodgram_api.wsgi:application", "--bind", "0:8000"]