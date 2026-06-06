package execution

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
)

// RunCommand executes a shell command in the specified directory.
func RunCommand(command, dir string) error {
	args := strings.Fields(command)
	if len(args) == 0 {
		return fmt.Errorf("empty command")
	}

	cmd := exec.Command(args[0], args[1:]...)
	cmd.Dir = dir
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	return cmd.Run()
}

// ProvisionDatabase is a placeholder for DB provisioning logic.
func ProvisionDatabase(dbType, name, user, password, host, port string) error {
	fmt.Printf("Provisioning %s database: %s at %s:%s\n", dbType, name, host, port)
	// TODO: Add actual provisioning logic (e.g., executing psql commands or docker run)
	return nil
}

// ManageVEnv is a placeholder for virtual environment management.
func ManageVEnv(name, dir string) error {
	fmt.Printf("Managing virtual environment %s in %s\n", name, dir)
	// python -m venv <name>
	cmd := fmt.Sprintf("python -m venv %s", name)
	return RunCommand(cmd, dir)
}
