from tortoise import Model, fields
from uuid import uuid4

class User(Model):
    id = fields.UUIDField(pk=True)
    polls = fields.ReverseRelation['Poll'] # one to many relation to poll

class Poll(Model):
    id = fields.UUIDField(pk=True)
    prompt = fields.TextField()
    active = fields.BooleanField(default=True)
    user = fields.ForeignKeyField("models.User", related_name="users") # one to one relation to user

class ProcessedResponse(Model):
    id = fields.UUIDField(pk=True)
    reason = fields.TextField()
    supports = fields.BooleanField() # stance on the issue
    poll: fields.ForeignKeyRelation[Poll] = fields.ForeignKeyField("models.Poll", related_name="polls_processed")

class ProcessedResponseNuance(Model):
    id = fields.UUIDField(pk=True)
    data = fields.TextField()
    processed_response: fields.ForeignKeyRelation[ProcessedResponse] = fields.ForeignKeyField("models.ProcessedResponse", related_name="processed_response")

class Response(Model):
    id = fields.UUIDField(pk=True)
    key = fields.UUIDField(default=uuid4, unique=True)
    data = fields.TextField(null=True)
    poll: fields.ForeignKeyRelation[Poll] = fields.ForeignKeyField("models.Poll", related_name="polls")