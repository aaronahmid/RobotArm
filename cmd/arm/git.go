package main

import (
	"os"
	"os/exec"

	"github.com/spf13/cobra"
)

var gitCmd = &cobra.Command{
	Use:                "git [args...]",
	Short:              "Execute a git command in the active project",
	DisableFlagParsing: true, // Passes all flags straight to git
	Run: func(cmd *cobra.Command, args []string) {
		wdir := getActiveProjectWDir()
		if wdir == "" {
			return
		}

		// Run git command in the working directory
		gitExec := exec.Command("git", args...)
		gitExec.Dir = wdir
		gitExec.Stdout = os.Stdout
		gitExec.Stderr = os.Stderr
		gitExec.Stdin = os.Stdin

		if err := gitExec.Run(); err != nil {
			// git will output its own error to Stderr
			os.Exit(1)
		}
	},
}

func init() {
	rootCmd.AddCommand(gitCmd)
}
