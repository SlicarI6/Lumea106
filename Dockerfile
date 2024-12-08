FROM python:3.11-slim

# Actualizează pachetele și instalează Firefox și dependențele
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    firefox-esr \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalează Geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz && \
    tar -xvzf /tmp/geckodriver.tar.gz -C /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

# Instalează Selenium
RUN pip install selenium

# Adaugă codul proiectului
WORKDIR /app
COPY . /app

# Comanda pentru rularea scriptului
CMD ["python3", "Lumea106.py"]
