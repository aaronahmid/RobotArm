.PHONY: build test clean release-snapshot

build:
	go build -o bin/arm cmd/arm/*.go

test:
	go test ./...

clean:
	rm -rf bin/ dist/ test-output/

release-snapshot:
	goreleaser release --snapshot --clean

release:
	goreleaser release --clean
