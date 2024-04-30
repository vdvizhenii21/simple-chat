FROM python:3.12.0
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app
ENV PYTHONPATH "${PYTHONPATH}:/app"
RUN python -m venv env
RUN pip install -r system/settings/requirements.txt
