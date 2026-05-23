IMAGE_NAME  ?= tourismo
IMAGE_TAG   ?= latest
REGISTRY    ?= ghcr.io/your-org
FULL_IMAGE   = $(REGISTRY)/$(IMAGE_NAME):$(IMAGE_TAG)
K8S_NS      = tourismo

# ── Docker ────────────────────────────────────────────────────────────────────
.PHONY: build push build-push

build:
	docker build -t $(FULL_IMAGE) .

push:
	docker push $(FULL_IMAGE)

build-push: build push

# ── Docker Compose (dev) ──────────────────────────────────────────────────────
.PHONY: up down logs restart

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

restart:
	docker compose restart django

# ── Kubernetes ────────────────────────────────────────────────────────────────
.PHONY: k8s-deploy k8s-rollout k8s-status k8s-logs k8s-shell k8s-migrate k8s-delete

k8s-deploy:
	kubectl apply -k k8s/

k8s-rollout:
	kubectl rollout restart deployment/django -n $(K8S_NS)
	kubectl rollout restart deployment/nginx  -n $(K8S_NS)

k8s-status:
	kubectl get pods,svc,ingress,hpa,pdb -n $(K8S_NS)

k8s-logs:
	kubectl logs -f deployment/django -n $(K8S_NS)

k8s-shell:
	kubectl exec -it deployment/django -n $(K8S_NS) -- /bin/sh

k8s-migrate:
	kubectl exec deployment/django -n $(K8S_NS) -- python manage.py migrate

k8s-delete:
	kubectl delete namespace $(K8S_NS)

# ── Image update helper ───────────────────────────────────────────────────────
.PHONY: deploy

deploy: build push
	kubectl set image deployment/django django=$(FULL_IMAGE) -n $(K8S_NS)
	kubectl rollout status deployment/django -n $(K8S_NS)
