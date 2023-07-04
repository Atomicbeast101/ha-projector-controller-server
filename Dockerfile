FROM python:3

# Add dependencies
RUN mkdir -p /app /logs /config
RUN pip install -r requirements.txt

# Copy files over
ADD app.py /app
ADD config.py /config
ADD bin /app

# Run
EXPOSE 5000/tcp
CMD ["python", "/app/app.py"]
