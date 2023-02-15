From python:3.9     

WORKDIR /app

#RUN python3 -m venv venv

#RUN source venv/bin/activate

RUN python -m pip install --upgrade pip

RUN pip install gunicorn

RUN pip install Flask

RUN pip install requests
#RUN pip install --upgrade os_sys 
#RUN pip install os_sys
ARG access
ENV access ${access}


COPY . .

EXPOSE 8000

CMD ["python3", "-m" , "main.py", "run", "--host=0.0.0.0"]
