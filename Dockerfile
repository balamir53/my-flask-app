FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# RUN pip install flask
# COPY . .
CMD ["flask","run","--host","0.0.0.0"]

# docker run -dp 5000:5000 -v "/c/Users/yusuf/my-flask-app:/app" my-flask-app:2.0
