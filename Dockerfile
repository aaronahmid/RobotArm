FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o arm cmd/arm/*.go

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/arm /usr/local/bin/arm

ENV ARM_API_HOST=0.0.0.0
ENV ARM_API_PORT=5555

EXPOSE 5555
CMD ["arm", "service", "run"]
