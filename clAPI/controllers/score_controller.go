package controllers

import (
	"clAPI/configs"
	"clAPI/models"
	"clAPI/responses"
	"context"
	"fmt"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var scoreCollection *mongo.Collection = configs.GetCollection(configs.DB, "scores")
var validate_score = validator.New()

func CreateScore() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		var score models.Score
		defer cancel()

		// validate the request body
		if err := c.BindJSON(&score); err != nil {
			c.JSON(http.StatusBadRequest, responses.ScoreResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		// use the validator library to validate required fields
		if validationErr := validate_score.Struct(&score); validationErr != nil {
			c.JSON(http.StatusBadRequest, responses.ScoreResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": validationErr.Error()}})
			return
		}

		newScore := models.Score{
			Player:      score.Player,
			Leaderboard: score.Leaderboard,
			HighScore:   score.HighScore,
		}

		result, err := scoreCollection.InsertOne(ctx, newScore)
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
		var score models.Score
		defer cancel()
		userId := c.Param("userId")
		leaderboard, bad := strconv.Atoi(c.Param("leaderboard"))
		if bad != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": bad.Error()}})
			return
		}

		objId, _ := primitive.ObjectIDFromHex(userId)

		// fmt.Println("Player Object: " + fmt.Sprint(objId))
		// fmt.Println("Leaderboard number: " + fmt.Sprint(leaderboard))

		filter := bson.M{"player": objId, "leaderboard": leaderboard}
		// query = append(query, bson.M{"player": objId}, bson.M{"leaderboard": leaderboard})
		// query := bson.M{"player": objId, "leaderboard": leaderboard}

		err := scoreCollection.FindOne(ctx, filter).Decode(&score)
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
		var score models.Score
		defer cancel()
		userId := c.Param("userId")
		leaderboard, bad := strconv.Atoi(c.Param("leaderboard"))
		if bad != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": bad.Error()}})
			return
		}

		objId, _ := primitive.ObjectIDFromHex(userId)

		// validate the request body
		if err := c.BindJSON(&score); err != nil {
			c.JSON(http.StatusBadRequest, responses.ScoreResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		// use the validator library to validate required fields
		if validationErr := validate_score.Struct(&score); validationErr != nil {
			c.JSON(http.StatusBadRequest, responses.ScoreResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": validationErr.Error()}})
			return
		}

		update := bson.M{"highscore": score.HighScore}
		result, err := scoreCollection.UpdateOne(ctx, bson.M{"player": objId, "leaderboard": leaderboard}, bson.M{"$set": update})
		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		// get updated user details
		var updatedScore models.Score
		if result.MatchedCount == 1 {
			err := scoreCollection.FindOne(ctx, bson.M{"player": objId, "leaderboard": leaderboard}).Decode(&updatedScore)
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
		defer cancel()
		leaderboard, bad := strconv.Atoi(c.Param("leaderboard"))
		if bad != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": bad.Error()}})
			return
		}

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
		leaderboard, bad := strconv.Atoi(c.Param("leaderboard"))
		if bad != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": bad.Error()}})
			return
		}

		results, err := scoreCollection.Find(ctx, bson.M{"leaderboard": leaderboard})

		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		// reading from the db in an optimal way
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

func GetTopTenBoardScores() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		var scores []models.Score
		defer cancel()
		leaderboard, bad := strconv.Atoi(c.Param("leaderboard"))
		if bad != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": bad.Error()}})
			return
		}
		docs, bad2 := strconv.Atoi(c.Param("docs"))
		if bad != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": bad2.Error()}})
			return
		}

		find_options := options.Find()
		find_options.SetSort(bson.D{{"highscore", -1}})
		find_options.SetLimit(int64(docs))
		results, err := scoreCollection.Find(ctx, bson.M{"leaderboard": leaderboard}, find_options)

		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.ScoreResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		// reading from the db in an optimal way
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

func MakeIndex() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()

		indexModel := mongo.IndexModel{
			Keys: bson.D{
				{"player", 1},
				{"leaderboard", 1},
			},
			Options: options.Index().SetUnique(true),
		}
		indexName, err1 := scoreCollection.Indexes().CreateOne(ctx, indexModel)
		if err1 != nil {
			panic(err1)
		}

		fmt.Println("Index name is: " + indexName)

		c.JSON(http.StatusOK, responses.ScoreResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"data": indexName}})
	}
}
