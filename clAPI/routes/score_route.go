package routes

import (
	"clAPI/controllers"
	"clAPI/middlewares"

	"github.com/gin-gonic/gin"
)

func ScoreRoute(router *gin.Engine) {

	// Score routes

	score := router.Group("/score").Use(middlewares.AuthUser())
	{
		score.POST("/:userId", controllers.CreateScore())
		score.GET("/:userId/:leaderboard", controllers.GetAScore())
		score.PUT("/:userId/:leaderboard", controllers.EditAScore())
		score.DELETE("/:userId/:leaderboard", controllers.DeleteAScore())
		// Testing endpoint for generating an Index
		// score.GET("/makeindex", controllers.MakeIndex())
	}

	scores := router.Group("/scores")
	{
		scores.GET("/:leaderboard", controllers.GetBoardScores())
		scores.GET("/limit/:docs/:leaderboard", controllers.GetTopTenBoardScores())
	}
}
