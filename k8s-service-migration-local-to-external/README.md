# Passo a Passo de Migração de Service no Kubernetes de Local para External

## 1️⃣ Limpar o Ambiente
```bash
kubectl delete ingress meu-ingress --ignore-not-found
kubectl delete service meu-servico --ignore-not-found
kubectl delete deployment nginx-deployment --ignore-not-found
```

## 2️⃣ Criar o Deployment e Service Local
```bash
kubectl create deployment nginx-deployment --image=nginx:latest
kubectl expose deployment nginx-deployment --name=meu-servico --port=80
```

## 3️⃣ Testar o Service Local (Acesso Direto no Cluster)
```bash
kubectl run -it --rm curlpod --image=curlimages/curl --restart=Never -- curl -v http://meu-servico
```

## 4️⃣ Criar o Ingress
Criar o arquivo **`ingress.yaml`**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: meu-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: meu-servico
            port:
              number: 80
```

Aplicar o Ingress:
```bash
kubectl apply -f ingress.yaml
```

## 5️⃣ Obter o IP do Service do Ingress Controller
### Windows (PowerShell)
```powershell
$INGRESS_IP = kubectl get svc -n ingress-nginx ingress-nginx-controller --output=jsonpath="{.spec.clusterIP}"
Write-Output $INGRESS_IP
```
### Linux/macOS
```bash
INGRESS_IP=$(kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.spec.clusterIP}')
echo $INGRESS_IP
```

## 6️⃣ Testar o acesso ao Ingress (apontando para o serviço local)
```bash
kubectl run -it --rm busybox --image=busybox --restart=Never -- wget -qO- --header="Host: meu-servico" http://$INGRESS_IP
```

## 7️⃣ Migrar o Serviço para ExternalName
```bash
kubectl delete service meu-servico
kubectl create service externalname meu-servico --external-name=example.com --tcp=80:80
```

## 8️⃣ Testar Acesso ao Serviço Externo via Ingress
```bash
kubectl run -it --rm busybox --image=busybox --restart=Never -- wget -qO- --header="Host: example.com" http://$INGRESS_IP
```
