# Passo a Passo de Migração de Service no OpenShift de Local para External

## 1️⃣ Limpar o Ambiente
```bash
oc delete route meu-route --ignore-not-found
oc delete service meu-servico --ignore-not-found
oc delete deployment nginx-deployment --ignore-not-found
```

## 2️⃣ Criar o Deployment e Service Local
```bash
oc new-app nginx:latest --name=nginx-deployment
oc expose dc/nginx-deployment --port=80
oc expose svc/nginx-deployment --name=meu-servico
```

## 3️⃣ Testar o Service Local (Acesso Direto no Cluster)
```bash
oc run -it --rm curlpod --image=curlimages/curl --restart=Never -- curl -v http://meu-servico
```

## 4️⃣ Criar a Route do OpenShift
Criar o arquivo **`route.yaml`**:
```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: meu-route
spec:
  to:
    kind: Service
    name: meu-servico
  port:
    targetPort: 80
  wildcardPolicy: None
```

Aplicar a Route:
```bash
oc apply -f route.yaml
```

## 5️⃣ Obter a URL da Route
```bash
ROUTE_URL=$(oc get route meu-route -o jsonpath='{.spec.host}')
echo $ROUTE_URL
```

## 6️⃣ Testar o Acesso à Route (Serviço Local)
```bash
oc run -it --rm busybox --image=busybox --restart=Never -- wget -qO- --header="Host: $ROUTE_URL" http://$ROUTE_URL
```

## 7️⃣ Migrar o Serviço para ExternalName
```bash
oc delete service meu-servico
oc create service externalname meu-servico --external-name=example.com --tcp=80:80
```

## 8️⃣ Testar Acesso ao Serviço Externo via Route
```bash
oc run -it --rm busybox --image=busybox --restart=Never -- wget -qO- --header="Host: example.com" http://$ROUTE_URL
```

