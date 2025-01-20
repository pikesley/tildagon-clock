FROM python:3.13

ARG APP

WORKDIR /opt/${APP}

COPY ./requirements.txt ${WORKDIR}

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY ./ ${WORKDIR}
