package state

import (
	"os"

	"gopkg.in/yaml.v3"
)

// ParseFile reads a YAML file and unmarshals it into a State struct.
func ParseFile(filePath string) (*State, error) {
	data, err := os.ReadFile(filePath)
	if err != nil {
		return nil, err
	}

	var s State
	err = yaml.Unmarshal(data, &s)
	if err != nil {
		return nil, err
	}

	return &s, nil
}
