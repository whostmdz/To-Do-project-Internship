# To-Do Project — Internship

Application To-Do développée avec Flask, PostgreSQL et Docker, avec supervision via Prometheus et Grafana.

Le déploiement de l'application est automatisé avec **Ansible**.

## Architecture

Le projet est composé de quatre services :

* **Flask** — application web To-Do
* **PostgreSQL** — base de données
* **Prometheus** — collecte des métriques
* **Grafana** — visualisation des métriques

Les services sont exécutés dans des conteneurs Docker et communiquent via un réseau Docker dédié.

```text
                    ┌─────────────────┐
                    │   Flask App     │
                    │   :5000         │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │   :5432         │
                    └─────────────────┘

                    ┌─────────────────┐
                    │   Prometheus    │
                    │   :9090         │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Grafana     │
                    │     :3000       │
                    └─────────────────┘
```

## Prerequisites

Before starting the project, make sure the following are installed:

* Docker
* Docker Compose
* Ansible

On Arch Linux:

```bash
sudo pacman -S docker docker-compose ansible
```

Make sure Docker is running:

```bash
sudo systemctl start docker
```

You can also enable Docker at startup:

```bash
sudo systemctl enable docker
```

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/whostmdz/To-Do-project-Internship.git
cd To-Do-project-Internship
```

### 2. Deploy with Ansible

Ansible is the main deployment method for this project.

```bash
cd ansible
ansible-playbook -i inventory.ini playbook.yml --ask-become-pass
```

The playbook automatically:

* creates the Docker network
* deploys PostgreSQL
* builds the Flask Docker image
* starts the Flask application
* deploys Prometheus
* deploys Grafana
* checks that the Flask application is responding

After deployment, the application is available at:

```text
http://localhost:5000
```

## Services

| Service           | URL                   |
| ----------------- | --------------------- |
| Flask application | http://localhost:5000 |
| Prometheus        | http://localhost:9090 |
| Grafana           | http://localhost:3000 |

### Grafana

Default credentials:

```text
Username: admin
Password: admin
```

To add Prometheus as a Grafana data source, use:

```text
http://todo_prometheus:9090
```

This address is used because Grafana communicates with Prometheus through the Docker network.

## Docker Containers

The Ansible deployment creates the following containers:

| Service    | Container         |
| ---------- | ----------------- |
| Flask      | `todo_flask`      |
| PostgreSQL | `todo_postgresql` |
| Prometheus | `todo_prometheus` |
| Grafana    | `todo_grafana`    |

All services use the Docker network:

```text
flask_network
```

## Managing the Application

### Check running containers

```bash
docker ps
```

### Stop the application

```bash
docker stop todo_flask todo_postgresql todo_prometheus todo_grafana
```

### Start the application again

```bash
docker start todo_postgresql todo_flask todo_prometheus todo_grafana
```

### Check Flask

```bash
curl http://localhost:5000
```

## Docker Compose

A `docker-compose.yml` file is also included in the repository.

It provides an alternative way of running the stack locally:

```bash
docker compose up
```

However, **Docker Compose and Ansible should not be used simultaneously to deploy the same services**, because both methods create and manage Docker containers and can cause conflicts with container names, networks, or ports.

For this project, **Ansible is the recommended deployment method**.

To stop a Compose deployment:

```bash
docker compose down
```

## Project Structure

```text
To-Do-project-Internship/
│
├── ansible/
│   ├── inventory.ini
│   ├── playbook.yml
│   ├── group_vars/
│   │   └── all.yml
│   └── roles/
│       ├── flask/
│       ├── postgresql/
│       ├── prometheus/
│       └── grafana/
│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── static/
│   └── templates/
│
├── prometheus/
│   └── prometheus.yml
│
├── docker-compose.yml
└── README.md
```

## Technologies

* Python
* Flask
* PostgreSQL
* Docker
* Docker Compose
* Ansible
* Prometheus
* Grafana

## Deployment

The deployment workflow is:

```text
Ansible
   │
   ├── Docker Network
   │
   ├── PostgreSQL
   │
   ├── Flask
   │
   ├── Prometheus
   │
   └── Grafana
```

The goal is to provide a reproducible deployment of the complete To-Do application and its monitoring stack using Ansible.
