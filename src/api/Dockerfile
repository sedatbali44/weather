FROM python:3.11

WORKDIR /src

COPY requirements.txt .


RUN apt-get update && apt-get install -y postgresql-client

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create a simple entrypoint script
RUN echo '#!/bin/bash\n\
echo "Waiting for PostgreSQL to be ready..."\n\
until PGPASSWORD=postgres psql -h db -U postgres -c "\\q"; do\n\
  echo "PostgreSQL is unavailable - sleeping"\n\
  sleep 1\n\
done\n\
echo "PostgreSQL is up - executing command"\n\
exec "$@"' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]