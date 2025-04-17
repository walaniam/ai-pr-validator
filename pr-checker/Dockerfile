FROM python:3.10-slim

EXPOSE 5050

WORKDIR /app

COPY app.py .

RUN pip install flask
RUN pip install requests

CMD ["python", "app.py"]
