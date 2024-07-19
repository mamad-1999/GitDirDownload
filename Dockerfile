FROM python:3.9-slim

# Create a non-root user
RUN useradd -m appuser

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for downloads and change its ownership
RUN mkdir /downloads && chown appuser:appuser /downloads

ENV NAME GitDirDownload

# Switch to the non-root user
USER appuser

WORKDIR /downloads

CMD ["python", "/app/github-download.py"]