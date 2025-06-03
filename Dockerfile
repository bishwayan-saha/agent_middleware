FROM python:3.13.3-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Update package list and install necessary tools
RUN apt-get update -y && \
apt-get install -y apt-transport-https curl gnupg

# Add Microsoft's package repository key
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -

# Add Microsoft's package repository
RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN ACCEPT_EULA=Y && apt-get upgrade -y && apt-get install -y msodbcsql17 mssql-tools

# Enable the ODBC driver and configure environment variables
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]