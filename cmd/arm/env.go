package main

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"

	"github.com/spf13/cobra"
)

var envCmd = &cobra.Command{
	Use:   "env",
	Short: "Manage virtual environments in the active project",
}

var envListCmd = &cobra.Command{
	Use:   "list",
	Short: "List virtual environments in the active project",
	Run: func(cmd *cobra.Command, args []string) {
		wdir := getActiveProjectWDir()
		if wdir == "" { return }

		fmt.Println("Virtual Environments:")
		entries, err := os.ReadDir(wdir)
		if err != nil { return }
		
		found := false
		for _, e := range entries {
			if e.IsDir() {
				if _, err := os.Stat(filepath.Join(wdir, e.Name(), "pyvenv.cfg")); err == nil {
					fmt.Printf("- %s\n", e.Name())
					found = true
				}
			}
		}
		if !found {
			fmt.Println("(No virtual environments found)")
		}
	},
}

var envCreateCmd = &cobra.Command{
	Use:   "create [name]",
	Short: "Create a new virtual environment in the active project",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		wdir := getActiveProjectWDir()
		if wdir == "" { return }

		name := args[0]
		fmt.Printf("Creating virtual environment '%s' in %s...\n", name, wdir)
		
		c := exec.Command("python3", "-m", "venv", name)
		c.Dir = wdir
		c.Stdout = os.Stdout
		c.Stderr = os.Stderr
		if err := c.Run(); err != nil {
			fmt.Printf("Failed to create environment: %v\n", err)
		} else {
			fmt.Println("Environment created successfully.")
		}
	},
}

var envDeleteCmd = &cobra.Command{
	Use:   "delete [name]",
	Short: "Delete a virtual environment in the active project",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		wdir := getActiveProjectWDir()
		if wdir == "" { return }

		name := args[0]
		envPath := filepath.Join(wdir, name)
		
		if _, err := os.Stat(filepath.Join(envPath, "pyvenv.cfg")); os.IsNotExist(err) {
			fmt.Printf("Error: '%s' is not a valid virtual environment.\n", name)
			return
		}

		fmt.Printf("Deleting virtual environment '%s'...\n", name)
		if err := os.RemoveAll(envPath); err != nil {
			fmt.Printf("Failed to delete environment: %v\n", err)
		} else {
			fmt.Println("Environment deleted successfully.")
		}
	},
}

var envActivateCmd = &cobra.Command{
	Use:   "activate [name]",
	Short: "Activate a virtual environment (spawns a subshell)",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		wdir := getActiveProjectWDir()
		if wdir == "" { return }

		name := args[0]
		envPath := filepath.Join(wdir, name)
		
		if _, err := os.Stat(filepath.Join(envPath, "pyvenv.cfg")); os.IsNotExist(err) {
			fmt.Printf("Error: '%s' is not a valid virtual environment.\n", name)
			return
		}

		fmt.Printf("Activating environment '%s'... (Type 'exit' to leave)\n", name)
		
		shell := os.Getenv("SHELL")
		if shell == "" {
			shell = "/bin/bash"
		}

		env := append(os.Environ(), fmt.Sprintf("VIRTUAL_ENV=%s", envPath))
		env = append(env, fmt.Sprintf("PATH=%s/bin:%s", envPath, os.Getenv("PATH")))

		c := exec.Command(shell)
		c.Env = env
		c.Dir = wdir
		c.Stdin = os.Stdin
		c.Stdout = os.Stdout
		c.Stderr = os.Stderr

		if err := c.Run(); err != nil {
			fmt.Printf("Subshell exited with error: %v\n", err)
		}
	},
}

func init() {
	rootCmd.AddCommand(envCmd)
	envCmd.AddCommand(envListCmd)
	envCmd.AddCommand(envCreateCmd)
	envCmd.AddCommand(envDeleteCmd)
	envCmd.AddCommand(envActivateCmd)
}
