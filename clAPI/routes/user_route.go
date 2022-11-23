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

		secure := user.Group("/secure").Use(middlewares.AuthUser())
		{
			secure.GET("/:userId", controllers.GetAUser())
			secure.PUT("/:userId", controllers.EditAUser())
			secure.DELETE("/:userId", controllers.DeleteAUser())
			secure.GET("/refresh/:userId", controllers.RefreshToken())

		}

		s2 := user.Group("/s2").Use(middlewares.Auth())
		{
			s2.GET("/all", controllers.GetAllUsers())
			s2.GET("/skedaddle", controllers.CheckToken())
		}
	}
}
