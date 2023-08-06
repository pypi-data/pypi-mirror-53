# Synopsis
This module is an add-on for Django REST Framework, based on Django LDP add-on. It serves django models for a notifications component, respecting the Linked Data Platform convention.
It aims at enabling people with little development skills to serve their own data, to be used with a LDP application.



# Models

## Notification
An object representing a notification. A notification has the following fields:

| Field     | Type                   | Default | Description                                               |
| --------- | ---------------------- | ------- | --------------------------------------------------------- |
| `user`    | `ForeignKey` to `User` |         | User targeted by the notification.                        |
| `author`  | `LDPUrlField`          |         | ID of the user at the origin of the notification          |
| `object`  | `LDPUrlField`          |         | ID of the object which is the subject of the notification |
| `type`    | `CharField`            |         | Short description of the notification                     |
| `summary` | `TextField`            |         | Longer description of the notification                    |
| `date`    | `DateTimeField`        | `now`   | Date of the notification                                  |
| `unread`  | `BooleanField`         | `True`  | Indicates that the notification has not been read yet.    |

NB: You can access to all the notifications of a User at `[host]/users/[id]/inbox`



## Subscription

An object allowing a User to be notified of any change on a resource or a container. A subscription has the following fields:

| Field    | Type       | Default | Description                                                  |
| -------- | ---------- | ------- | ------------------------------------------------------------ |
| `object` | `URLField` |         | ID of the resource or the container to watch                 |
| `inbox`  | `URLField` |         | ID of the inbox to notify when the resource or the container change |



# Signals

## Create notification on subscribed objects

When an object is saved, a notification is created for all the subscriptions related to this object.



## Send email when new notification

When a notification is created, an email is sent to the user.