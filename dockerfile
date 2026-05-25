FROM python:3.12-slim

WORKDIR /app

# No dependencies to install — just the source
COPY . .

# Run as a non-root user
RUN useradd --create-home appuser
USER appuser

EXPOSE 8080

CMD ["python", "main.py"]
