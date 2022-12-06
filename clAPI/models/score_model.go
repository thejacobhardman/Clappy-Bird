package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Score struct {
	Player      primitive.ObjectID `json:"player" validate:"required"`
	Username    string             `json:"username" validate:"required"`
	Leaderboard int                `json:"leaderboard" validate:"required"`
	HighScore   int                `json:"highscore" validate:"gte=0"`
}
