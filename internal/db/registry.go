package db

import (
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/aaronahmid/robotarm/internal/state"
	"github.com/glebarez/sqlite"
	"gorm.io/gorm"
)

type ProjectState struct {
	ID           uint      `gorm:"primaryKey"`
	Name         string    `gorm:"uniqueIndex;not null"`
	Language     string
	Framework    string
	Architecture string
	WDir         string    `gorm:"not null"`
	CreatedAt    time.Time
	UpdatedAt    time.Time
}

var DB *gorm.DB

func InitDB() error {
	dbPath := os.Getenv("ARM_DB_PATH")
	if dbPath == "" {
		home, err := os.UserHomeDir()
		if err != nil {
			return err
		}
		dataDir := filepath.Join(home, ".robotarm", "data")
		if err := os.MkdirAll(dataDir, 0755); err != nil {
			return err
		}
		dbPath = filepath.Join(dataDir, "robotarm.db")
	}

	fmt.Printf("Connecting to registry database at %s\n", dbPath)
	database, err := gorm.Open(sqlite.Open(dbPath), &gorm.Config{})
	if err != nil {
		return fmt.Errorf("failed to connect to database: %w", err)
	}

	err = database.AutoMigrate(&ProjectState{})
	if err != nil {
		return fmt.Errorf("failed to migrate database: %w", err)
	}

	DB = database
	return nil
}

func RegisterProject(s *state.State) error {
	project := ProjectState{
		Name:         s.Name,
		Language:     s.Language,
		Framework:    s.Framework,
		Architecture: s.Architecture,
		WDir:         s.WDir,
	}

	// Update if exists, otherwise create
	result := DB.Where(ProjectState{Name: project.Name}).Assign(project).FirstOrCreate(&project)
	return result.Error
}

func ListProjects() ([]ProjectState, error) {
	var projects []ProjectState
	result := DB.Find(&projects)
	return projects, result.Error
}

func GetProjectByName(name string) (ProjectState, error) {
	var project ProjectState
	result := DB.Where(ProjectState{Name: name}).First(&project)
	return project, result.Error
}
