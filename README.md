# Flask Todo — Docker + Ansible + Prometheus + Grafana

A todo list application built with Flask and PostgreSQL,
monitored with Prometheus and Grafana,
deployed automatically with Ansible.

## Stack

- Python 3.12 / Flask
- PostgreSQL 15
- Prometheus
- Grafana
- Docker
- Ansible

## Requirements

- Docker
- Ansible
- ansible-galaxy collection install community.docker

## Quick start

### Manual (Docker only)

# Create the network
docker network create flask_net

# Start PostgreSQL
docker run -d \
  --name todo_postgres \
  --network flask_net \
  -e POSTGRES_DB=tododb \
  -e POSTGRES_USER=todouser \
  -e POSTGRES_PASSWORD=todopass \
  postgres:15-alpine

# Build and start Flask
cd app
docker build -t todo-app .
docker run -p 5000:5000 \
  --name todo_flask \
  --network flask_net \
  -e DATABASE_URL=postgresql://todouser:todopass@todo_postgres:5432/tododb \
  todo-app

# Start Prometheus
docker run -d \
  --name todo_prometheus \
  --network flask_net \
  -p 9090:9090 \
  -v $(pwd)/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Start Grafana
docker run -d \
  --name todo_grafana \
  --network flask_net \
  -p 3000:3000 \
  grafana/grafana

### Automated (Ansible)

cd ansible
ansible-playbook -i inventory.ini playbook.yml

## Services

| Service    | URL                      |
|------------|--------------------------|
| Flask app  | http://localhost:5000    |
| Prometheus | http://localhost:9090    |
| Grafana    | http://localhost:3000    |

## Notes

- Grafana default credentials: admin / admin
- Add Prometheus as data source: http://todo_prometheus:9090
- SSL certificate issues on corporate networks:
  pip install uses --trusted-host flags in the Dockerfile
