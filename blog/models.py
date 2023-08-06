from django.db import models
from django.utils import timezone

from users.models import User

# Create your models here.
class Post(models.Model):
	"""
	model post to store the blog post data
	"""
    
	types = (
		('public', 'Public'),
		('private', 'Private')
	)
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	type = models.CharField(max_length=10, choices=types)


	class Meta:
		db_table = 'Post'
		verbose_name = "Post"
		permissions = [
            ("list_post", "Can list post"),
                  
            ]
            

	def __str__(self):
		return f"Title: {self.title}"
	
 
class Like(models.Model):
    """
	model like to store the like data of users and posts
	"""
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='liked_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Like'
        verbose_name = 'Like'
        permissions = [
            ]

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
