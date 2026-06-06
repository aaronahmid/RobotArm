package environment

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/aaronahmid/robotarm/internal/state"
)

func ProvisionDatabases(s *state.State) error {
	if len(s.Databases) == 0 {
		return nil
	}

	fmt.Println("Provisioning databases via docker-compose...")

	var composeLines []string
	composeLines = append(composeLines, "services:")

	for _, db := range s.Databases {
		dbType := strings.ToLower(db.Type)
		if dbType == "postgresql" || dbType == "postgres" {
			composeLines = append(composeLines, fmt.Sprintf("  %s:", db.Name))
			composeLines = append(composeLines, "    image: postgres:15-alpine")
			composeLines = append(composeLines, "    environment:")
			composeLines = append(composeLines, fmt.Sprintf("      - POSTGRES_USER=%s", db.User))
			composeLines = append(composeLines, fmt.Sprintf("      - POSTGRES_PASSWORD=%s", db.Password))
			composeLines = append(composeLines, "    ports:")
			composeLines = append(composeLines, fmt.Sprintf("      - \"%s:5432\"", db.Port))
		}
	}

	composeContent := strings.Join(composeLines, "\n")
	composePath := filepath.Join(s.WDir, "docker-compose.yml")

	if err := os.WriteFile(composePath, []byte(composeContent), 0644); err != nil {
		return err
	}

	fmt.Printf("Generated %s\n", composePath)
	return nil
}
