package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type FullUser struct {
	Id         primitive.ObjectID `json:"id,omitempty"`
	Username   string             `json:"username,omitempty" validate:"required"`
	Password   string             `json:"password,omitempty" validate:"required"`
	FriendCode string             `json:"friendcode,omitempty" validate:"required"`
}

type User struct {
	Id         primitive.ObjectID `json:"id,omitempty"`
	Username   string             `json:"username,omitempty" validate:"required"`
	FriendCode string             `json:"friendcode,omitempty" validate:"required"`
}
