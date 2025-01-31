FROM python:3.13.1

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . ./

EXPOSE 8050
CMD ["python", "app.py"]