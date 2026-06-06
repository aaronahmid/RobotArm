package state

type State struct {
	Name         string     `yaml:"name"`
	Version      string     `yaml:"version"`
	Language     string     `yaml:"language"`
	Framework    string     `yaml:"framework"`
	Architecture string     `yaml:"architecture"`
	Git          string     `yaml:"git"`
	GitSSH       string     `yaml:"git_ssh"`
	WDir         string     `yaml:"wdir"`
	PackageManager string     `yaml:"package_manager"`
	VEnvs        []VEnv     `yaml:"venvs"`
	Databases    []Database `yaml:"databases"`
	Tests        []Test     `yaml:"tests"`
	Pipelines    []Pipeline `yaml:"pipelines,omitempty"`
}

type VEnv struct {
	Name     string `yaml:"name"`
	Dir      string `yaml:"dir"`
	OnCreate bool   `yaml:"on_create"`
}

type Database struct {
	Name     string `yaml:"name"`
	Type     string `yaml:"type"`
	User     string `yaml:"user"`
	Password string `yaml:"password"`
	Host     string `yaml:"host"`
	Port     string `yaml:"port"`
	OnCreate bool   `yaml:"on_create"`
}

type Test struct {
	Tool      string `yaml:"tool"`
	Discovery string `yaml:"discovery"`
	TestDir   string `yaml:"test_dir"`
}

type Pipeline struct {
	Name  string `yaml:"name"`
	Steps []Step `yaml:"steps"`
}

type Step struct {
	Run string `yaml:"run"`
}
