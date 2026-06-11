## Quick start

### With Docker Compose (recommended)

git clone <your-repo>
cd my_project
docker compose up

### With Ansible

cd ansible
ansible-playbook -i inventory.ini playbook.yml

## Services

| Service    | URL                    |
|------------|------------------------|
| Flask app  | http://localhost:5000  |
| Prometheus | http://localhost:9090  |
| Grafana    | http://localhost:3000  |

Grafana default credentials: admin / admin
Add Prometheus as data source: http://todo_prometheus:9090
