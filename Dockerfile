FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/

COPY ./start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./production_start /production_start
RUN sed -i 's/\r//' /production_start
RUN chmod +x /production_start