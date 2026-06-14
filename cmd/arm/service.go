package main

import (
	"embed"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"runtime/debug"
	"strings"

	"github.com/aaronahmid/robotarm/internal/api"
	"github.com/spf13/cobra"
)

//go:embed embedded/Dockerfile embedded/docker-compose.yml
var embeddedFiles embed.FS

func serviceDir() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".robotarm", "service")
}

// prepareServiceDir writes the embedded Dockerfile and docker-compose.yml to
// ~/.robotarm/service/ and ensures a Linux arm binary is present for the Docker
// build context, regardless of the caller's working directory or host OS.
func prepareServiceDir() error {
	dir := serviceDir()
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("creating service dir: %w", err)
	}

	if isReleasedBuild() {
		compose := releaseCompose()
		if err := os.WriteFile(filepath.Join(dir, "docker-compose.yml"), []byte(compose), 0644); err != nil {
			return fmt.Errorf("writing docker-compose.yml: %w", err)
		}
		return nil
	}

	for _, name := range []string{"Dockerfile", "docker-compose.yml"} {
		data, err := embeddedFiles.ReadFile("embedded/" + name)
		if err != nil {
			return fmt.Errorf("reading embedded %s: %w", name, err)
		}
		if err := os.WriteFile(filepath.Join(dir, name), data, 0644); err != nil {
			return fmt.Errorf("writing %s: %w", name, err)
		}
	}

	dst := filepath.Join(dir, "arm")
	if runtime.GOOS == "linux" {
		execPath, err := os.Executable()
		if err != nil {
			return fmt.Errorf("resolving executable path: %w", err)
		}
		if err := copyFile(execPath, dst); err != nil {
			return fmt.Errorf("copying binary: %w", err)
		}
	} else {
		if err := buildLinuxBinary(dst); err != nil {
			return fmt.Errorf("building Linux binary for Docker: %w", err)
		}
	}

	return nil
}

// buildLinuxBinary cross-compiles an amd64 Linux binary to dst.
// It finds the source by: (1) walking up from CWD, (2) a previously saved
// source path, or (3) go install from the module proxy for released builds.
func buildLinuxBinary(dst string) error {
	env := append(os.Environ(), "GOOS=linux", "GOARCH=amd64", "CGO_ENABLED=0")

	if root, err := resolveSourceDir(); err == nil {
		cmd := exec.Command("go", "build", "-o", dst, "./cmd/arm")
		cmd.Dir = root
		cmd.Env = env
		cmd.Stderr = os.Stderr
		return cmd.Run()
	}

	info, ok := debug.ReadBuildInfo()
	if !ok {
		return fmt.Errorf("cannot determine build info; run once from the project source directory to register it")
	}
	version := info.Main.Version
	if version == "(devel)" {
		return fmt.Errorf("source directory unknown — run arm service start once from within the project directory")
	}

	cmd := exec.Command("go", "install", info.Main.Path+"/cmd/arm@"+version)
	cmd.Env = append(env, "GOBIN="+filepath.Dir(dst))
	cmd.Stderr = os.Stderr
	return cmd.Run()
}

// resolveSourceDir finds the module root by walking up from CWD. If found it
// saves the path for future invocations from unrelated directories.
func resolveSourceDir() (string, error) {
	home, _ := os.UserHomeDir()
	savedPath := filepath.Join(home, ".robotarm", "source_dir")

	if root, err := findGoModRoot(); err == nil {
		_ = os.WriteFile(savedPath, []byte(root), 0644)
		return root, nil
	}

	data, err := os.ReadFile(savedPath)
	if err != nil {
		return "", fmt.Errorf("no saved source path")
	}
	root := strings.TrimSpace(string(data))
	if _, err := os.Stat(filepath.Join(root, "go.mod")); err != nil {
		return "", fmt.Errorf("saved source path no longer valid: %s", root)
	}
	return root, nil
}

func releaseCompose() string {
	image := "ghcr.io/aaronahmid/robotarm:" + releaseImageTag()
	return `services:
  api:
    image: ` + image + `
    ports:
      - "5555:5555"
    environment:
      - ARM_API_HOST=0.0.0.0
      - ARM_API_PORT=5555
      - ARM_DB_PATH=/data/robotarm.db
    volumes:
      - ~/.robotarm/data:/data
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=krumitz
      - POSTGRES_PASSWORD=robotarm
      - POSTGRES_DB=robotarm_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
`
}

func isReleasedBuild() bool {
	info, ok := debug.ReadBuildInfo()
	return ok && info.Main.Version != "" && info.Main.Version != "(devel)"
}

func releaseImageTag() string {
	info, ok := debug.ReadBuildInfo()
	if !ok || info.Main.Version == "(devel)" {
		return "latest"
	}
	return info.Main.Version
}

func findGoModRoot() (string, error) {
	dir, err := os.Getwd()
	if err != nil {
		return "", err
	}
	for {
		if _, err := os.Stat(filepath.Join(dir, "go.mod")); err == nil {
			return dir, nil
		}
		parent := filepath.Dir(dir)
		if parent == dir {
			return "", fmt.Errorf("go.mod not found")
		}
		dir = parent
	}
}

func copyFile(src, dst string) error {
	in, err := os.Open(src)
	if err != nil {
		return err
	}
	defer in.Close()

	out, err := os.OpenFile(dst, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0755)
	if err != nil {
		return err
	}
	defer out.Close()

	_, err = io.Copy(out, in)
	return err
}

func runDockerCompose(args ...string) error {
	if err := prepareServiceDir(); err != nil {
		return fmt.Errorf("preparing service directory: %w", err)
	}
	dir := serviceDir()
	composeFile := filepath.Join(dir, "docker-compose.yml")
	fullArgs := append([]string{"-f", composeFile}, args...)
	cmd := exec.Command("docker-compose", fullArgs...)
	cmd.Dir = dir
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd.Run()
}

var serviceCmd = &cobra.Command{
	Use:   "service",
	Short: "Manage the RobotArm API service",
	Long:  `Start, stop, and check the status of the background API service via Docker Compose.`,
	Run: func(cmd *cobra.Command, args []string) {
		cmd.Help()
	},
}

var serviceRunCmd = &cobra.Command{
	Use:    "run",
	Short:  "Run the API service natively (internal use)",
	Hidden: true,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Running native API server...")
		if err := api.StartServer(); err != nil {
			fmt.Println("Error starting server:", err)
		}
	},
}

var serviceStartCmd = &cobra.Command{
	Use:   "start",
	Short: "Start the API service containers",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Starting API service containers...")
		if err := runDockerCompose("up", "-d", "--build"); err != nil {
			fmt.Println("Error starting service:", err)
		}
	},
}

var serviceStopCmd = &cobra.Command{
	Use:   "stop",
	Short: "Stop the API service containers",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Stopping API service containers...")
		if err := runDockerCompose("down"); err != nil {
			fmt.Println("Error stopping service:", err)
		}
	},
}

var serviceStatusCmd = &cobra.Command{
	Use:   "status",
	Short: "Check the status of the API service containers",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Checking API service status...")
		if err := runDockerCompose("ps"); err != nil {
			fmt.Println("Error checking status:", err)
		}
	},
}

func init() {
	rootCmd.AddCommand(serviceCmd)
	serviceCmd.AddCommand(serviceRunCmd)
	serviceCmd.AddCommand(serviceStartCmd)
	serviceCmd.AddCommand(serviceStopCmd)
	serviceCmd.AddCommand(serviceStatusCmd)
}
