# build app
FROM python:3.10-slim AS build-stage

WORKDIR /
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

EXPOSE 4444

ARG APP_ENV=$APP_ENV

ENV PYTHONUNBUFFERED 1
ENV MY_VAR=$APP_ENV

#RUN echo $APP_ENV

#CMD ["python", "run_bot.py", "$MY_VAR"]
CMD ["/bin/bash", "-c", "python run_bot.py $MY_VAR"]
#CMD python run_bot.py $APP_ENV