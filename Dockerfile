FROM python:3.8



    

ADD quiera.py /
ADD brooklyn.db /

ADD requirements.txt /

RUN pip install -r requirements.txt


ENTRYPOINT [ "python" ]
CMD [  "quiera.py" ]