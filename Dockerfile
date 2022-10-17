FROM python
ENV PYTHONNUNBUFFERED=1
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .
EXPOSE 8000
