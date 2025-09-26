FROM python:alpine3.18 AS base

# Set BUILD ARGS (to be overwritten at build time).
# Set as placeholder values (T212_API_TOKEN not an actual secret value).
ARG T212_API_TOKEN="1234adiadimai23923"
ARG T212_BASE_API_PATH="https://demo.trading212.com/api/v0/"
ARG RETAIN_DATA_FOR_DAYS=1000


# Set ENVS FROM BUILD ARGS (Allow us to set our environment variables dynamically).
ENV T212_API_TOKEN=$T212_API_TOKEN
ENV T212_BASE_API_PATH=$T212_BASE_API_PATH
ENV RETAIN_DATA_FOR_DAYS=$RETAIN_DATA_FOR_DAYS

# Set workdir.
WORKDIR /app

FROM base AS python_setup

# Copy requirements.txt and use it to install dependencies.
# I SHOULD GENERATE A NEW requirements.txt before any merge.
COPY requirements.txt .
RUN pip3 install -r requirements.txt

FROM python_setup AS main

# Copy over everything from current dir
COPY src/ .

# Expose port that flask runs on as default.
EXPOSE 5000

# Set command to run our application (flask based) on all localhost IP's i.e. 127.0.0.1 & 172.0.0.X.
CMD [ "python3", "-m" , "flask", "--app", "src/main" ,"run", "--host=0.0.0.0"]
