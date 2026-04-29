# Projeto FastAPI - Gerenciamento de Tarefas (DevOps)

Este projeto demonstra um fluxo completo de CI/CD utilizando FastAPI, Docker e Kubernetes.

## Tecnologias Utilizadas
- **FastAPI**: API moderna e rápida.
- **Docker**: Containerização da aplicação.
- **GitHub Actions**: Automação de CI/CD (Lint, Testes, Build, Push).
- **Kubernetes**: Orquestração de containers.

## Como Executar Localmente (Docker)
1. Construa a imagem: `docker build -t minha-app .`
2. Rode o container: `docker run -p 8000:8000 minha-app`

## Como Implantar no Kubernetes (usando Minikube)
1. Inicie o Minikube:
   ```bash
   minikube start
   ```
2. (Opcional) Use o daemon do Docker do Minikube para construir imagens localmente:
   ```bash
   eval $(minikube docker-env)
   docker build -t seu-usuario/minha-app-fastapi:latest .
   ```
3. Aplique os manifestos:
   ```bash
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```
4. Verifique o status:
   ```bash
   kubectl get pods
   kubectl get services
   ```
5. Acesse a aplicação:
   ```bash
   minikube service fastapi-service
   ```
