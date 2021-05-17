FROM python:3.8-slim-buster

# We copy just the requirements.txt first to leverage Docker cache
WORKDIR /app
ENV FLASK_RUN_PORT=7778
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 7778
COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]