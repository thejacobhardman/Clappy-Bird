package routes

import (
	"clAPI/controllers"

	"github.com/gin-gonic/gin"
)

func UserRoute(router *gin.Engine) {

	// User routes
	router.POST("/user", controllers.CreateUser())
	router.GET("/user/:userId", controllers.GetAUser())
	router.PUT("/user/:userId", controllers.EditAUser())
	router.DELETE("/user/:userId", controllers.DeleteAUser())
	router.GET("/users", controllers.GetAllUsers())

	// Score routes
	router.POST("/score", controllers.CreateScore())
	router.GET("/score/:userId/:leaderboard", controllers.GetAScore())
	router.PUT("/score/:userId/:leaderboard", controllers.EditAScore())
	router.DELETE("/score/:userId/:leaderboard", controllers.DeleteAScore())
	router.GET("/scores/:leaderboard", controllers.GetBoardScores())
	router.GET("/scores/makeindex", controllers.MakeIndex())
}
