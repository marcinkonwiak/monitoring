# Monitoring Server

---

## Running locally:

Install `uv`:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Run the server:    
```bash
uv run manage.py runserver
```

Run the gRPC server:    
```bash
uv run manage.py grpcrunaioserver --dev
```


## Generating proto files:

```bash
uv run manage.py generateproto
```
