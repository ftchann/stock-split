FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir result
COPY . .
CMD ["pwd"]
CMD ["python3", "src/stock_split.py"]