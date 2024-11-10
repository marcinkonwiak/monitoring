# Monitoring Server

---

## Running locally:

```bash
go run cmd/main.go
```

## Generating proto files:

```bash
protoc --proto_path=proto proto/*.proto --go_out=. --go-grpc_out=.
```
