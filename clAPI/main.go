package main

import (
	"clAPI/configs"
	"clAPI/routes"

	// "time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	// set CORS
	config := cors.Default()

	/*config := cors.New(cors.Config{
		AllowOrigins:     []string{"0.0.0.0"},
		AllowAllOrigins:  true,
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE"},
		AllowHeaders:     []string{"Origin"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		AllowOriginFunc: func(origin string) bool {
			return origin == "0.0.0.0"
		},
		MaxAge: 12 * time.Hour,
	})*/

	router.Use(config)

	configs.ConnectDB()

	routes.UserRoute(router)
	routes.ScoreRoute(router)

	// Get port from .env
	port := configs.EnvHostPort()

	router.Run(":" + port)
}
