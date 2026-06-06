package main

import (
	"fmt"
	"github.com/spf13/cobra"
)

var execCmd = &cobra.Command{
	Use:   "command [cmd]",
	Short: "Execute a management command",
	Long:  `Run management commands (like django manage.py) in the active environment.`,
	Args:  cobra.MinimumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("Executing command: %v\n", args)
		// TODO: Implement command execution logic
	},
}

func init() {
	rootCmd.AddCommand(execCmd)
}
