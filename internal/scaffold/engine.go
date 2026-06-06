package scaffold

import (
	"embed"
	"fmt"
	"strings"

	"github.com/aaronahmid/robotarm/internal/state"
)

//go:embed templates/*
var TemplatesFS embed.FS

// Generate handles the scaffolding logic based on the provided State.
func Generate(s *state.State) error {
	lang := strings.ToLower(s.Language)
	framework := strings.ToLower(s.Framework)
	arch := strings.ToLower(s.Architecture)

	fmt.Printf("Scaffolding %s/%s project with %s architecture in %s\n", lang, framework, arch, s.WDir)

	switch lang {
	case "go", "golang":
		return GenerateGoProject(s)
	case "python":
		return GeneratePythonProject(s)
	default:
		return fmt.Errorf("unsupported language: %s", s.Language)
	}
}
