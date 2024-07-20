FROM python:3.9-slim

RUN useradd -m appuser
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

ENV NAME GitDirDownload

USER appuser
CMD ["python", "github-download.py"]