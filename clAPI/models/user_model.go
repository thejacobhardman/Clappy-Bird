package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type User struct {
	Id         primitive.ObjectID `json:"id,omitempty"`
	Username   string             `json:"username,omitempty" validate:"required"`
	Password   string             `json:"password,omitempty" validate:"required"`
	FriendCode string             `json:"friendcode,omitempty" validate:"required"`
	Points     int                `json:"points,omitempty" validate:"required"`
}
