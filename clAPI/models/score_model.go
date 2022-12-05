package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Score struct {
	Player      primitive.ObjectID `json:"player,omitempty" validate:"required"`
	Username    string             `json:"username,omitempty" validate:"required"`
	Leaderboard int                `json:"leaderboard,omitempty" validate:"required"`
	HighScore   int                `json:"highscore,omitempty" validate:"gte=0"`
}
