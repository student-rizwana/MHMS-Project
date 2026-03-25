from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg




class Maid(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='maid_profile', null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    photo = models.CharField(max_length=255, blank=True)
    skills = models.TextField()  # comma separated: Cleaning, Cooking
    experience = models.IntegerField()  # years
    location = models.CharField(max_length=100)

    availability = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    def __str__(self):
        return self.name

    def update_avg_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        self.avg_rating = round(float(avg or 0), 2)
        self.save(update_fields=['avg_rating'])

class Review(models.Model):
    maid = models.ForeignKey(Maid, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1,6)], default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.rating}/5 - {self.maid.name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.maid.update_avg_rating()

