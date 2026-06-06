package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
)

func getActiveProjectWDir() string {
	home, err := os.UserHomeDir()
	if err != nil {
		fmt.Printf("Error getting home directory: %v\n", err)
		return ""
	}

	activeStateBytes, err := os.ReadFile(filepath.Join(home, ".robotarm", "active_state"))
	if err != nil {
		fmt.Println("Error: No active state found. Run 'arm state activate <name>' first.")
		return ""
	}
	activeState := string(activeStateBytes)

	resp, err := http.Get(fmt.Sprintf("http://localhost:5555/api/v1/states/get?name=%s", activeState))
	if err != nil || resp.StatusCode != http.StatusOK {
		fmt.Printf("Error: State '%s' not found in registry. Is the API service running?\n", activeState)
		return ""
	}
	defer resp.Body.Close()

	var project map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&project); err != nil {
		fmt.Println("Error parsing API response:", err)
		return ""
	}

	wdir, ok := project["WDir"].(string)
	if !ok || wdir == "" {
		fmt.Println("Error: Invalid working directory from API")
		return ""
	}
	return wdir
}
