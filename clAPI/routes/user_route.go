package routes

import (
	"clAPI/controllers"
	"clAPI/middlewares"

	"github.com/gin-gonic/gin"
)

func UserRoute(router *gin.Engine) {

	// User routes

	user := router.Group("/user")
	{
		user.POST("/register", controllers.CreateUser())
		user.GET("/auth", controllers.AuthenticateUser())
		/* Testing endpoints for generating Indexes
		user.GET("/index/username", controllers.MakeIndexUsername())
		user.GET("/index/friendcode", controllers.MakeIndexCode())
		*/

		secure := user.Group("/secure").Use(middlewares.Auth())
		{
			secure.GET("/:userId", controllers.GetAUser())
			secure.PUT("/:userId", controllers.EditAUser())
			secure.DELETE("/:userId", controllers.DeleteAUser())
			secure.GET("/all", controllers.GetAllUsers())
		}
	}
}
