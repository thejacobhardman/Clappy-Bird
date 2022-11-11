package main

import (
	"clAPI/configs"
	"clAPI/routes"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	configs.ConnectDB()

	routes.UserRoute(router)
	routes.ScoreRoute(router)

	router.Run("localhost:8000")
}
