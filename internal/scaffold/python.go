package scaffold

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"strings"
	"text/template"

	"github.com/aaronahmid/robotarm/internal/state"
)

func GeneratePythonProject(s *state.State) error {
	framework := strings.ToLower(s.Framework)
	arch := strings.ToLower(s.Architecture)

	if framework == "fastapi" && arch == "clean" {
		return generatePythonFastAPIClean(s)
	}

	return fmt.Errorf("unsupported python configuration: framework=%s architecture=%s", framework, arch)
}

func generatePythonFastAPIClean(s *state.State) error {
	fmt.Println("Generating Python/FastAPI/Clean project...")

	baseDir := "templates/python/fastapi/clean"

	err := fs.WalkDir(TemplatesFS, baseDir, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}

		if d.IsDir() {
			return nil
		}

		// Read template content
		content, err := TemplatesFS.ReadFile(path)
		if err != nil {
			return err
		}

		// Parse template
		tmpl, err := template.New(path).Parse(string(content))
		if err != nil {
			return err
		}

		// Determine output path
		relPath, _ := filepath.Rel(baseDir, path)
		outPath := filepath.Join(s.WDir, strings.TrimSuffix(relPath, ".tmpl"))

		// Create output directory
		if err := os.MkdirAll(filepath.Dir(outPath), 0755); err != nil {
			return err
		}

		// Write output file
		outFile, err := os.Create(outPath)
		if err != nil {
			return err
		}
		defer outFile.Close()

		return tmpl.Execute(outFile, s)
	})

	return err
}
