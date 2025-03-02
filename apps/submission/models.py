from django.db import models

class Submission(models.Model):
    class Meta:
        verbose_name_plural = 'Submissions'

    comment_count = models.IntegerField()
    sales_count = models.IntegerField()
    average_rating = models.FloatField()

    def __str__(self):
        return "Submission Requirements"
