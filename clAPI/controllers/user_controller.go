package controllers

import (
	"clAPI/auth"
	"clAPI/configs"
	"clAPI/models"
	"clAPI/responses"

	"context"
	// "fmt"
	"crypto/sha256"
	"encoding/hex"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	// "go.mongodb.org/mongo-driver/mongo/options"
)

var userCollection *mongo.Collection = configs.GetCollection(configs.DB, "users")
var validate_user = validator.New()

func CreateUser() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		var user models.FullUser
		defer cancel()

		// validate the request body
		if err := c.BindJSON(&user); err != nil {
			c.JSON(http.StatusBadRequest, responses.UserResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		// use the validator library to validate required fields
		if validationErr := validate_user.Struct(&user); validationErr != nil {
			c.JSON(http.StatusBadRequest, responses.UserResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": validationErr.Error()}})
			return
		}

		a := []byte(configs.EnvS1() + user.Password + configs.EnvS2())
		b := sha256.Sum256(a)
		newPass := hex.EncodeToString(b[:])

		newUser := models.FullUser{
			Id:         primitive.NewObjectID(),
			Username:   user.Username,
			Password:   newPass,
			FriendCode: user.FriendCode,
		}

		result, err := userCollection.InsertOne(ctx, newUser)
		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.UserResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		c.JSON(http.StatusCreated, responses.UserResponse{Status: http.StatusCreated, Message: "success", Data: map[string]interface{}{"data": map[string]interface{}{"InsertedID": newUser.Id, "result": result}}})
	}
}

func GetAUser() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		userId := c.Param("userId")
		var user models.User
		defer cancel()

		objId, _ := primitive.ObjectIDFromHex(userId)

		err := userCollection.FindOne(ctx, bson.M{"id": objId}).Decode(&user)
		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.UserResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		c.JSON(http.StatusOK, responses.UserResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"data": user}})
	}
}

func EditAUser() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		userId := c.Param("userId")
		var user models.FullUser
		defer cancel()
		objId, _ := primitive.ObjectIDFromHex(userId)

		// validate the request body
		if err := c.BindJSON(&user); err != nil {
			c.JSON(http.StatusBadRequest, responses.UserResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		// use the validator library to validate required fields
		if validationErr := validate_user.Struct(&user); validationErr != nil {
			c.JSON(http.StatusBadRequest, responses.UserResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": validationErr.Error()}})
			return
		}

		a := []byte(configs.EnvS1() + user.Password + configs.EnvS2())
		b := sha256.Sum256(a)
		newPass := hex.EncodeToString(b[:])

		update := bson.M{"username": user.Username, "password": newPass, "friendcode": user.FriendCode}
		result, err := userCollection.UpdateOne(ctx, bson.M{"id": objId}, bson.M{"$set": update})
		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.UserResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		// get updated user details
		var updatedUser models.User
		if result.MatchedCount == 1 {
			err := userCollection.FindOne(ctx, bson.M{"id": objId}).Decode(&updatedUser)
			if err != nil {
				c.JSON(http.StatusInternalServerError, responses.UserResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
				return
			}
		}

		c.JSON(http.StatusOK, responses.UserResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"data": updatedUser}})
	}
}

func DeleteAUser() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		userId := c.Param("userId")
		defer cancel()

		objId, _ := primitive.ObjectIDFromHex(userId)

		result, err := userCollection.DeleteOne(ctx, bson.M{"id": objId})
		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.UserResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		if result.DeletedCount < 1 {
			c.JSON(http.StatusNotFound,
				responses.UserResponse{Status: http.StatusNotFound, Message: "error", Data: map[string]interface{}{"data": "User with specified ID not found!"}},
			)
			return
		}

		c.JSON(http.StatusOK,
			responses.UserResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"data": "User successfully deleted!"}},
		)
	}
}

func GetAllUsers() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		var users []models.User
		defer cancel()

		results, err := userCollection.Find(ctx, bson.M{})

		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.UserResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			return
		}

		// reading from the db in an optimal way
		defer results.Close(ctx)
		for results.Next(ctx) {
			var singleUser models.User
			if err = results.Decode(&singleUser); err != nil {
				c.JSON(http.StatusInternalServerError, responses.UserResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error()}})
			}

			users = append(users, singleUser)
		}

		c.JSON(http.StatusOK, responses.UserResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"data": users}})
	}
}

func AuthenticateUser() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		var user_auth models.UserAuth
		var user models.User
		defer cancel()

		// validate the request body
		if err := c.BindJSON(&user_auth); err != nil {
			c.JSON(http.StatusBadRequest, responses.UserResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": err.Error(), "token": ""}})
			return
		}

		// use the validator library to validate required fields
		if validationErr := validate_user.Struct(&user_auth); validationErr != nil {
			c.JSON(http.StatusBadRequest, responses.UserResponse{Status: http.StatusBadRequest, Message: "error", Data: map[string]interface{}{"data": validationErr.Error(), "token": ""}})
			return
		}

		a := []byte(configs.EnvS1() + user_auth.Password + configs.EnvS2())
		b := sha256.Sum256(a)
		newPass := hex.EncodeToString(b[:])

		err := userCollection.FindOne(ctx, bson.M{"username": user_auth.Username, "password": newPass}).Decode(&user)
		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.UserResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": "Invalid credentials", "token": ""}})
			return
		}

		tokenString, err := auth.GenerateJWT(string(user.Id.Hex()))
		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.UserResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error(), "token": tokenString}})
		}

		c.JSON(http.StatusOK, responses.UserResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"data": user, "token": tokenString}})
	}
}

func RefreshToken() gin.HandlerFunc {
	return func(c *gin.Context) {

		userId := c.Param("userId")

		tokenString, err := auth.GenerateJWT(userId)
		if err != nil {
			c.JSON(http.StatusInternalServerError, responses.UserResponse{Status: http.StatusInternalServerError, Message: "error", Data: map[string]interface{}{"data": err.Error(), "token": tokenString}})
		}

		c.JSON(http.StatusOK, responses.UserResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"token": tokenString}})
	}
}

func CheckToken() gin.HandlerFunc {
	return func(c *gin.Context) {

		c.JSON(http.StatusOK, responses.UserResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"data": "skedoodle"}})

	}
}

// Deprecated Test Functions
/*

func MakeIndexUsername() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()

		indexModel := mongo.IndexModel{
			Keys: bson.D{
				{"username", 1},
			},
			Options: options.Index().SetUnique(true),
		}
		indexName, err1 := userCollection.Indexes().CreateOne(ctx, indexModel)
		if err1 != nil {
			panic(err1)
		}

		fmt.Println("Index name is: " + indexName)

		c.JSON(http.StatusOK, responses.UserResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"data": indexName}})
	}
}

func MakeIndexCode() gin.HandlerFunc {
	return func(c *gin.Context) {
		ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()

		indexModel := mongo.IndexModel{
			Keys: bson.D{
				{"friendcode", 1},
			},
			Options: options.Index().SetUnique(true),
		}
		indexName, err1 := userCollection.Indexes().CreateOne(ctx, indexModel)
		if err1 != nil {
			panic(err1)
		}

		fmt.Println("Index name is: " + indexName)

		c.JSON(http.StatusOK, responses.UserResponse{Status: http.StatusOK, Message: "success", Data: map[string]interface{}{"data": indexName}})
	}
}

*/
