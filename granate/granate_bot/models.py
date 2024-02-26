from django.db import models

# Create your models here.
class Question(models.Model):
    id =models.AutoField(primary_key=True)
    chat_id = models.BigIntegerField()
    question = models.TextField()
    answered = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.id} {self.chat_id} {self.answered}"

    class Meta:
        db_table = 'Question' 

class User(models.Model):
    id =models.AutoField(primary_key=True)
    chat_id = models.BigIntegerField()
    admin = models.BooleanField(default = False)
    get_notified = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.id} {self.chat_id}"

    class Meta:
        db_table = 'User' 