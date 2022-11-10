package routes

import (
	"clAPI/controllers"

	"github.com/gin-gonic/gin"
)

func ScoreRoute(router *gin.Engine) {

	// Score routes
	router.POST("/score", controllers.CreateScore())
	router.GET("/score/:userId/:leaderboard", controllers.GetAScore())
	router.PUT("/score/:userId/:leaderboard", controllers.EditAScore())
	router.DELETE("/score/:userId/:leaderboard", controllers.DeleteAScore())
	router.GET("/scores/:leaderboard", controllers.GetBoardScores())
	router.GET("/scoreslimit/:docs/:leaderboard", controllers.GetTopTenBoardScores())
	router.GET("/scores/makeindex", controllers.MakeIndex())
}
