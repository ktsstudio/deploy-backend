FROM python:3.9

RUN apt update && apt -y install gettext-base
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ./run.sh
