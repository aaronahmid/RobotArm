package main

import (
	"embed"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"

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
// ~/.robotarm/service/ and copies the current arm binary there so the Docker
// build context is self-contained regardless of the caller's working directory.
func prepareServiceDir() error {
	dir := serviceDir()
	if err := os.MkdirAll(dir, 0755); err != nil {
		return fmt.Errorf("creating service dir: %w", err)
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

	execPath, err := os.Executable()
	if err != nil {
		return fmt.Errorf("resolving executable path: %w", err)
	}
	if err := copyFile(execPath, filepath.Join(dir, "arm")); err != nil {
		return fmt.Errorf("copying binary: %w", err)
	}

	return nil
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
	cmd := exec.Command("docker-compose", args...)
	cmd.Dir = serviceDir()
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
