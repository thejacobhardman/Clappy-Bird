package configs

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

func EnvMongoURI() string {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	return os.Getenv("MONGOURI")
}

func EnvEncKey() string {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	return os.Getenv("ENCKEY")
}

func EnvS1() string {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	return os.Getenv("S1")
}

func EnvS2() string {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	return os.Getenv("S2")
}

func EnvHostPort() string {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file, default port used (8080)")
		return "8080"
	}
	return os.Getenv("PORT")
}
