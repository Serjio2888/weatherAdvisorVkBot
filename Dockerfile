FROM python:3.7

WORKDIR /usr/src/app/weatherAdvisorVkBot

RUN pip3 install pytz
RUN pip3 install vk_api
RUN pip3 install psycopg2

COPY . .

CMD python3 weather.py

