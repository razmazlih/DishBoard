FROM python:3.12.4

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["gunicorn", "-b", "0.0.0.0:8000", "dish_board.wsgi:application"]