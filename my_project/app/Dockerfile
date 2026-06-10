FROM python:3.12-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org
COPY . .
EXPOSE 5000
CMD ["python", "-u", "app.py"]
