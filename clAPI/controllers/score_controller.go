package controllers

import (
	"clAPI/configs"
	"clAPI/models"
	"clAPI/responses"
	"context"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
)

var scoreCollection *mongo.Collection = configs.GetCollection(configs.DB, "scores")
var validate_score = validator.New()

func CreateScore() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		var score models.Score
		defer cancel()

		//validate the request body
		if err := c.BindJSON(&score); err != nil {
			c.JSON(http.StatusBadRequest, responses.ScoreResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		//use the validator library to validate required fields
		if validationErr := validate_score.Struct(&score); validationErr != nil {
			c.JSON(http.StatusBadRequest, responses.ScoreResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": validationErr.Error()}})
			return
		}

		newScore := models.Score{
			Player:      score.Player,
			Leaderboard: score.Leaderboard,
			HighScore:   score.HighScore,
		}

		result, err := userCollection.InsertOne(ctx, newScore)
		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		c.JSON(http.StatusCreated, responses.ScoreResponse{Status: http.StatusCreated, Message: "success", Data: map[string]interface{}{"data": result}})
	}
}

func GetAScore() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		userId := c.Param("userId")
		leaderboard := c.Param("leaderboard")
		var score models.Score
		defer cancel()

		objId, _ := primitive.ObjectIDFromHex(userId)

		err := scoreCollection.FindOne(ctx, bson.M{"player": objId, "leaderboard": leaderboard}).Decode(&score)
		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		c.JSON(http.StatusOK, responses.ScoreResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"data": score}})
	}
}

func EditAScore() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		userId := c.Param("userId")
		leaderboard := c.Param("leaderboard")
		var score models.Score
		defer cancel()
		objId, _ := primitive.ObjectIDFromHex(userId)

		//validate the request body
		if err := c.BindJSON(&score); err != nil {
			c.JSON(http.StatusBadRequest, responses.ScoreResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		//use the validator library to validate required fields
		if validationErr := validate_score.Struct(&score); validationErr != nil {
			c.JSON(http.StatusBadRequest, responses.ScoreResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": validationErr.Error()}})
			return
		}

		update := bson.M{"player": score.Player, "leaderboard": score.Leaderboard, "high_score": score.HighScore}
		result, err := scoreCollection.UpdateOne(ctx, bson.M{"player": objId, "leaderboard": leaderboard}, bson.M{"$set": update})
		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		//get updated user details
		var updatedScore models.Score
		if result.MatchedCount == 1 {
			err := userCollection.FindOne(ctx, bson.M{"player": objId, "leaderboard": leaderboard}).Decode(&updatedScore)
			if err != nil {
				c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
				return
			}
		}

		c.JSON(http.StatusOK, responses.ScoreResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"data": updatedScore}})
	}
}

func DeleteAScore() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		userId := c.Param("userId")
		leaderboard := c.Param("leaderboard")
		defer cancel()

		objId, _ := primitive.ObjectIDFromHex(userId)

		result, err := scoreCollection.DeleteOne(ctx, bson.M{"player": objId, "leaderboard": leaderboard})
		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		if result.DeletedCount < 1 {
			c.JSON(http.StatusNotFound,
				responses.ScoreResponse{Status: http.StatusNotFound, Message: "error", Data: map[string]interface{}{"data": "Score with specified UserID/Leaderboard not found!"}},
			)
			return
		}

		c.JSON(http.StatusOK,
			responses.ScoreResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"data": "Score successfully deleted!"}},
		)
	}
}

func GetBoardScores() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		var scores []models.Score
		defer cancel()

		results, err := scoreCollection.Find(ctx, bson.M{})

		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		//reading from the db in an optimal way
		defer results.Close(ctx)
		for results.Next(ctx) {
			var singleScore models.Score
			if err = results.Decode(&singleScore); err != nil {
				c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			}

			scores = append(scores, singleScore)
		}

		c.JSON(http.StatusOK,
			responses.ScoreResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"data": scores}},
		)
	}
}
