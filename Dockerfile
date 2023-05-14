From python:3.9     

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install -r ${PWD}/requirements.txt

ARG access
ENV access ${access}


COPY . .

EXPOSE 3000

EXPOSE 8191

CMD ["python3", "-m" , "main", "run", "--host=0.0.0.0"]
