package api

import (
	"fmt"
	"net/http"
	"os"
	"github.com/aaronahmid/robotarm/internal/db"
)

func StartServer() error {
	if err := db.InitDB(); err != nil {
		return fmt.Errorf("failed to init database: %w", err)
	}

	host := os.Getenv("ARM_API_HOST")
	if host == "" {
		host = "0.0.0.0"
	}
	port := os.Getenv("ARM_API_PORT")
	if port == "" {
		port = "5555"
	}

	mux := http.NewServeMux()
	RegisterHandlers(mux)

	addr := fmt.Sprintf("%s:%s", host, port)
	fmt.Printf("Starting API service on %s\n", addr)
	return http.ListenAndServe(addr, mux)
}
