package main

import (
	"fmt"
	"github.com/spf13/cobra"
)

var testCmd = &cobra.Command{
	Use:   "test",
	Short: "Run tests for the active state",
	Long:  `Run tests as defined in the active yaml state configuration.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Running tests...")
		// TODO: Implement test runner logic
	},
}

func init() {
	rootCmd.AddCommand(testCmd)
}
