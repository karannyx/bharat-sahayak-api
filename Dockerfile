# Python 3.11 ka halka version use karenge
FROM python:3.11-slim

# Container ke andar kaam karne ka folder
WORKDIR /app

# Sabse pehle libraries install karenge
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki saara backend code copy karenge
COPY . .

# Port 8000 ko bahar access ke liye open karenge
EXPOSE 8000

# Backend ko start karne ki command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]