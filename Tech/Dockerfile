FROM python:3.11-slim
WORKDIR /tech
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "uvicorn", "main:words", "--reload", "--host", "0.0.0.0", "--port", "8000"]
