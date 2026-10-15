from django.db import models
# from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    headline = models.CharField()
    body = models.TextField()
    author = models.ForeignKey('auth.User',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True
                            )
    published_at = models.DateTimeField(auto_now=True)
    #author_email = models.EmailField(

       # null=True, # Makes the column optional. Database-specific feature
       # default="any_author@email.com", # The fixed data that is used when the input is not provided
       # blank=True, # Form-specific
       # unique=True, # If true, Provision of the same data twice is unacceptable
       # max_length=10, # Enforces the maximum number of characters
       # choices={"M": "Male", "F": "Female"}
       # choices={"test@email.com": "Author Test Email"}

       #)
  
    def __str__(self):
        return self.headline