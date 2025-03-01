FROM python:3.11

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create wait-for-db script
COPY <<'EOT' /usr/local/bin/wait-for-db.sh
#!/bin/bash
set -e

host="${DATABASE_URL##*@}"
host="${host%%/*}"
host="${host%%:*}"

echo "Waiting for PostgreSQL to be ready at: $host"
until PGPASSWORD=postgres psql -h "$host" -U postgres -c '\q'; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - executing command"
exec "$@"
EOT

RUN chmod +x /usr/local/bin/wait-for-db.sh

COPY . .

ENTRYPOINT ["wait-for-db.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]