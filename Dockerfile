FROM python:alpine3.18

# Set workdir
WORKDIR /app

# Copy requirements.txt and use it to install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy over everything from current dir
COPY . .

# Expose port that flask runs on as default
EXPOSE 5000

# Set command to run our application (flask based) on all localhost IP's i.e. 127.0.0.1 & 172.0.0.X
CMD [ "python3", "-m" , "flask", "--app", "src/main" ,"run", "--host=0.0.0.0"]