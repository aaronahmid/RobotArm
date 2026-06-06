package environment

import (
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/aaronahmid/robotarm/internal/execution"
	"github.com/aaronahmid/robotarm/internal/state"
)

func SetupRuntime(s *state.State) error {
	lang := strings.ToLower(s.Language)

	switch lang {
	case "go", "golang":
		fmt.Println("Running go mod tidy...")
		return execution.RunCommand("go mod tidy", s.WDir)
	case "node":
		fmt.Println("Running npm install...")
		return execution.RunCommand("npm install", s.WDir)
	case "python":
		venvName := "venv"
		for _, v := range s.VEnvs {
			if v.OnCreate && v.Name != "" {
				venvName = v.Name
				break
			}
		}

		fmt.Printf("Setting up Python virtual environment '%s'...\n", venvName)
		if err := execution.RunCommand(fmt.Sprintf("python3 -m venv %s", venvName), s.WDir); err != nil {
			return err
		}

		pm := strings.ToLower(s.PackageManager)
		if pm == "poetry" {
			fmt.Println("Installing dependencies via poetry...")
			execution.RunCommand("poetry init -n", s.WDir)
			
			content, err := os.ReadFile(s.WDir + "/requirements.txt")
			if err == nil {
				deps := strings.Fields(string(content))
				if len(deps) > 0 {
					cmdArgs := append([]string{"add"}, deps...)
					cmd := exec.Command("poetry", cmdArgs...)
					cmd.Dir = s.WDir
					cmd.Stdout = os.Stdout
					cmd.Stderr = os.Stderr
					return cmd.Run()
				}
			}
			return nil
		} else if pm == "pipenv" {
			fmt.Println("Installing dependencies via pipenv...")
			return execution.RunCommand("pipenv install -r requirements.txt", s.WDir)
		} else {
			fmt.Println("Installing dependencies via pip...")
			pipCmd := fmt.Sprintf("./%s/bin/pip install -r requirements.txt", venvName)
			return execution.RunCommand(pipCmd, s.WDir)
		}
	}
	return nil
}

func SetupGit(s *state.State) error {
	gitURL := s.Git
	if s.GitSSH != "" {
		gitURL = s.GitSSH
	}

	if gitURL == "" {
		return nil // No git config provided
	}

	fmt.Println("Initializing Git repository...")
	if err := execution.RunCommand("git init", s.WDir); err != nil {
		return fmt.Errorf("failed to git init: %w", err)
	}

	fmt.Printf("Adding remote origin: %s\n", gitURL)
	if err := execution.RunCommand(fmt.Sprintf("git remote add origin %s", gitURL), s.WDir); err != nil {
		return fmt.Errorf("failed to add git remote: %w", err)
	}

	fmt.Println("Creating initial commit...")
	execution.RunCommand("git add .", s.WDir)
	
	commitCmd := exec.Command("git", "commit", "-m", "Initial commit by RobotArm")
	commitCmd.Dir = s.WDir
	commitCmd.Stdout = os.Stdout
	commitCmd.Stderr = os.Stderr
	commitCmd.Run()

	return nil
}
