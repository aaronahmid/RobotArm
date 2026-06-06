package main

import (
	"fmt"
	"os"
	"os/exec"

	"github.com/aaronahmid/robotarm/internal/api"
	"github.com/spf13/cobra"
)

var serviceCmd = &cobra.Command{
	Use:   "service",
	Short: "Manage the RobotArm API service",
	Long:  `Start, stop, and check the status of the background API service via Docker Compose.`,
	Run: func(cmd *cobra.Command, args []string) {
		cmd.Help()
	},
}

var serviceRunCmd = &cobra.Command{
	Use:   "run",
	Short: "Run the API service natively (internal use)",
	Hidden: true,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Running native API server...")
		if err := api.StartServer(); err != nil {
			fmt.Println("Error starting server:", err)
		}
	},
}

// helper to run docker-compose commands
func runDockerCompose(args ...string) error {
	cmd := exec.Command("docker-compose", args...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	return cmd.Run()
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
