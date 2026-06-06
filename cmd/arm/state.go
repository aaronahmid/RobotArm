package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"path/filepath"

	"github.com/spf13/cobra"

	"github.com/aaronahmid/robotarm/internal/environment"
	"github.com/aaronahmid/robotarm/internal/scaffold"
	"github.com/aaronahmid/robotarm/internal/state"
)

var stateCmd = &cobra.Command{
	Use:   "state",
	Short: "Manage RobotArm states",
	Long:  `Create, list, and activate development environment states.`,
	Run: func(cmd *cobra.Command, args []string) {
		cmd.Help()
	},
}

var stateCreateCmd = &cobra.Command{
	Use:   "create [file]",
	Short: "Create a state from a yaml file",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		file := args[0]
		fmt.Printf("Creating state from %s\n", file)

		s, err := state.ParseFile(file)
		if err != nil {
			fmt.Printf("Error parsing state file: %v\n", err)
			return
		}

		if err := scaffold.Generate(s); err != nil {
			fmt.Printf("Error scaffolding project: %v\n", err)
			return
		}

		if err := environment.ProvisionDatabases(s); err != nil {
			fmt.Printf("Error provisioning databases: %v\n", err)
			return
		}

		if err := environment.SetupRuntime(s); err != nil {
			fmt.Printf("Error setting up runtime: %v\n", err)
			return
		}

		if err := environment.SetupGit(s); err != nil {
			fmt.Printf("Error setting up Git: %v\n", err)
			// Continue even if git fails
		}

		// Register with the background API
		jsonData, err := json.Marshal(s)
		if err == nil {
			resp, err := http.Post("http://localhost:5555/api/v1/states/register", "application/json", bytes.NewBuffer(jsonData))
			if err != nil {
				fmt.Println("Warning: Could not register project with global registry. Is the API service running? (arm service start)")
			} else {
				resp.Body.Close()
			}
		}

		fmt.Println("State creation successful!")
	},
}

var stateListCmd = &cobra.Command{
	Use:   "list",
	Short: "List globally managed states",
	Run: func(cmd *cobra.Command, args []string) {
		resp, err := http.Get("http://localhost:5555/api/v1/states")
		if err != nil {
			fmt.Println("Error: API service is unreachable. Make sure to run 'arm service start'")
			return
		}
		defer resp.Body.Close()

		var projects []map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&projects); err != nil {
			fmt.Println("Error parsing response:", err)
			return
		}

		fmt.Println("REGISTERED PROJECTS:")
		for _, p := range projects {
			fmt.Printf("- %v [%v/%v]: %v\n", p["Name"], p["Language"], p["Framework"], p["WDir"])
		}
	},
}

var stateActivateCmd = &cobra.Command{
	Use:   "activate [state_id]",
	Short: "Activate a specific state",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		stateID := args[0]
		
		// Verify project exists
		resp, err := http.Get(fmt.Sprintf("http://localhost:5555/api/v1/states/get?name=%s", stateID))
		if err != nil || resp.StatusCode != http.StatusOK {
			fmt.Printf("Error: State '%s' not found in registry. Is the API service running?\n", stateID)
			return
		}
		defer resp.Body.Close()

		home, err := os.UserHomeDir()
		if err != nil {
			fmt.Printf("Error getting home directory: %v\n", err)
			return
		}

		err = os.MkdirAll(filepath.Join(home, ".robotarm"), 0755)
		if err == nil {
			err = os.WriteFile(filepath.Join(home, ".robotarm", "active_state"), []byte(stateID), 0644)
		}

		if err != nil {
			fmt.Printf("Error saving active state: %v\n", err)
			return
		}

		fmt.Printf("Successfully activated state: %s\n", stateID)
	},
}

func init() {
	rootCmd.AddCommand(stateCmd)
	stateCmd.AddCommand(stateCreateCmd)
	stateCmd.AddCommand(stateListCmd)
	stateCmd.AddCommand(stateActivateCmd)
}
