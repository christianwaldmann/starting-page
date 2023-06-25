FROM python:3.9-buster
EXPOSE 80
WORKDIR /App
COPY requirements.txt /App
RUN pip install -r requirements.txt
COPY . /App
CMD ["./start.sh"]
