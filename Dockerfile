FROM python:3

# Add dependencies
RUN mkdir -p /app /logs /config
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy files over
ADD bin /app
ADD app.py /app

# Run
EXPOSE 5000/tcp
CMD ["python", "/app/app.py"]
