# Passo a Passo de Migração de Service no Kubernetes de Local para External

## 1. Criar o Deployment com Nginx (Local)

Crie um Deployment chamado `nginx-deployment` utilizando a imagem `nginx:latest`:

```bash
kubectl create deployment nginx-deployment --image=nginx:latest
```

## 2. Criar o Service Local (ClusterIP)

Exponha o Deployment criando um Service ClusterIP chamado `meu-servico` na porta 80:

```bash
kubectl expose deployment nginx-deployment --name=meu-servico --port=80
```

## 3. Testar o Service Local com Curl

Utilize um container que contenha o `curl` para testar o acesso ao Service:

```bash
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- curl -v http://meu-servico
```

**Observação:**  
Nesta etapa, a requisição é feita para o Service que direciona para o Nginx local, portanto, a resposta deverá ser a página padrão do Nginx.

## 4. Remover o Service Local

Exclua o Service `meu-servico`:

```bash
kubectl delete service meu-servico
```

## 5. Criar o Service Externo (ExternalName) Apontando para example.com

Crie um novo Service chamado `meu-servico` do tipo `ExternalName` que aponta para `example.com` na porta 80:

```bash
kubectl create service externalname meu-servico --external-name=example.com --tcp=80:80
```

## 6. Testar o Service Externo com Curl (Ajustando o Cabeçalho Host)

Utilize um container com `curl` para testar o acesso ao novo Service. Como o Service do tipo `ExternalName` apenas resolve para o domínio externo, é necessário ajustar o cabeçalho `Host` para que o destino aceite a requisição:

```bash
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- curl -v http://meu-servico -H "Host: example.com"
```

### Explicação:

- Na etapa 3, o `curl` é executado sem customizar o header `Host`, pois o Service local (`ClusterIP`) encaminha a requisição para o Deployment do Nginx, que responde normalmente.
- Na etapa 6, o header `Host` é ajustado para `example.com` para que o servidor remoto aceite a requisição, já que a resolução DNS do Service do tipo `ExternalName` retorna `example.com`.
