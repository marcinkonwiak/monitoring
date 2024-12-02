package cmd

import (
	"fmt"
	"github.com/marcinkonwiak/monitoring-client/client"
	"github.com/spf13/cobra"
)

var startCmd = &cobra.Command{
	Use:   "start",
	Short: "Start the client",
	Run: func(cmd *cobra.Command, args []string) {
		server, _ := cmd.Flags().GetString("server")
		interval, _ := cmd.Flags().GetInt("interval")
		err := validateInterval(interval)
		if err != nil {
			fmt.Printf("Error: %v\n", err)
			return
		}

		fmt.Printf("Starting monitoring on server: %s\n", server)
		client.NewClient(server, interval).Start()
	},
}

func init() {
	startCmd.Flags().StringP("server", "s", "localhost:50051", "Server address")
	startCmd.Flags().IntP("interval", "i", 1, "Interval in seconds")
	rootCmd.AddCommand(startCmd)
}

func validateInterval(interval int) error {
	if interval < 1 {
		return fmt.Errorf("interval must be greater than 0")
	}
	return nil
}
