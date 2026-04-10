# Student Result Portal – DevOps Project
**Subject:** 24CS2018 – DevOps | **Semester:** VII CSE (2025–2026 Odd Semester)
**Faculty:** Dr. E. Bijolin Edwin

---

## Project Title
**Automated CI/CD Pipeline for a Student Result Portal using Docker, Kubernetes, and Azure**

## Project Overview
A Flask-based web application that displays student examination results, deployed end-to-end using a full DevOps pipeline: GitHub Actions for CI/CD, Docker for containerization, Terraform for infrastructure provisioning on Azure, Ansible for configuration management, and Kubernetes (AKS) for orchestration.

---

## Tools & Technologies
| Tool | Purpose |
|---|---|
| Python Flask | Web application |
| Git / GitHub | Version control |
| GitHub Actions | CI/CD pipeline |
| Docker | Containerization |
| Azure ACR | Container registry |
| Terraform | Infrastructure as Code |
| Ansible | Configuration management |
| Kubernetes (AKS) | Container orchestration |

---

## Project Structure
```
student-result-portal/
├── app/
│   └── app.py                   # Flask application
├── templates/
│   ├── base.html
│   ├── index.html               # Results table
│   └── detail.html              # Per-student detail
├── tests/
│   └── test_app.py              # Pytest unit tests
├── k8s/
│   ├── deployment.yml           # Kubernetes Deployment
│   ├── service.yml              # LoadBalancer Service
│   └── hpa.yml                  # Horizontal Pod Autoscaler
├── terraform/
│   └── main.tf                  # Azure infra (RG + ACR + AKS)
├── ansible/
│   └── deploy-playbook.yml      # Ansible deployment playbook
├── .github/workflows/
│   └── deploy.yml               # GitHub Actions CI/CD workflow
├── Dockerfile                   # Multi-stage Docker build
├── requirements.txt
└── README.md
```

---

## Phase-by-Phase Setup

### Phase 1 – Source Control
```bash
git clone https://github.com/<your-username>/student-result-portal
cd student-result-portal
git checkout -b dev
# make changes
git add .
git commit -m "feat: initial flask app"
git push origin dev
# open a pull request to main on GitHub
```

### Phase 2 – Containerization
```bash
# Build image locally
docker build -t student-result-portal:local .

# Run and test locally
docker run -p 5000:5000 student-result-portal:local
# Open http://localhost:5000

# Push to ACR (after Terraform phase)
az acr login --name studentportalacr
docker tag student-result-portal:local studentportalacr.azurecr.io/student-result-portal:latest
docker push studentportalacr.azurecr.io/student-result-portal:latest
```

### Phase 3 – Infrastructure (Terraform)
```bash
cd terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan

# After project evaluation, destroy resources
terraform destroy
```

### Phase 4 – Configuration Management (Ansible)
```bash
pip install ansible kubernetes
ansible-galaxy collection install community.kubernetes

# Get AKS kubeconfig first
az aks get-credentials --resource-group studentportal-rg --name studentportal-aks

ansible-playbook ansible/deploy-playbook.yml \
  -e "image_tag=latest" \
  -e "acr_name=studentportalacr"
```

### Phase 5 – CI/CD Pipeline (GitHub Actions)
Add these secrets in **GitHub → Settings → Secrets and variables → Actions:**

| Secret | Value |
|---|---|
| `AZURE_CREDENTIALS` | Output of `az ad sp create-for-rbac ...` |
| `ACR_NAME` | `studentportalacr` |
| `AZURE_RESOURCE_GROUP` | `studentportal-rg` |
| `AKS_CLUSTER_NAME` | `studentportal-aks` |

Generate Azure credentials:
```bash
az ad sp create-for-rbac \
  --name "github-actions-sp" \
  --role contributor \
  --scopes /subscriptions/<subscription-id> \
  --sdk-auth
```

Pipeline triggers automatically on every push to `main`.

### Phase 6 – Verify Deployment
```bash
kubectl get pods -n student-portal
kubectl get svc -n student-portal
# Copy the EXTERNAL-IP from the service output
# Open http://<EXTERNAL-IP> in your browser
```

---

## Running Tests Locally
```bash
pip install -r requirements.txt
pytest tests/ -v
```

---

## GitHub Actions Pipeline Flow
```
Code Push → Test → Build Docker Image → Push to ACR → Ansible Deploy → Verify on AKS
```

---

## Expected Outcomes
- ✅ App accessible via public LoadBalancer IP
- ✅ Automated deployment on every `git push`
- ✅ Zero-downtime rolling updates
- ✅ Auto-scaling via HPA (2–5 pods based on CPU)
- ✅ Health checks via `/health` endpoint
