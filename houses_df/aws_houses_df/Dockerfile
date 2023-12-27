FROM python:3.9

# Set working directory in the container
WORKDIR /app

# Copy model code and requirements file
COPY model.py /app/model.py
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Define command to run your model (for example)
CMD ["python", "model.py"]
