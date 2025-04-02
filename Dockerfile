# Use official Python image
FROM python:3.9

# Set working directory in container
WORKDIR /app

# Copy project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
# RUN mkdir -p /app/staticfiles
RUN python manage.py collectstatic --noinput

# Expose port 8000 (default for Django)
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
