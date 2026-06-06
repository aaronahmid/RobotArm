package main

import (
	"fmt"
	"github.com/spf13/cobra"
)

var pipelineCmd = &cobra.Command{
	Use:   "pipeline",
	Short: "Manage and run CI/CD pipelines locally",
	Long:  `Run local CI/CD pipelines defined in the yaml configuration.`,
	Run: func(cmd *cobra.Command, args []string) {
		cmd.Help()
	},
}

var pipelineRunCmd = &cobra.Command{
	Use:   "run [pipeline_name]",
	Short: "Run a specific pipeline",
	Args:  cobra.ExactArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("Running pipeline: %s\n", args[0])
		// TODO: Implement local task runner for pipeline
	},
}

func init() {
	rootCmd.AddCommand(pipelineCmd)
	pipelineCmd.AddCommand(pipelineRunCmd)
}
