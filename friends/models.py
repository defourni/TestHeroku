from django.db import models
from django.utils import timezone
from users.models import User

class Friend(models.Model):
    '''
    A pair of users can only have less than two Friend instaces, since there are only following status:
    One-way follow (followee not yet approved): not_read=True
    One-way follow (followee rejected): not_read=False
    Friend (mutual/two-way following): the followee should also create a Friend instance and mark both instances with mutual=True
    Unfollow: delete the Friend instance and mark the followee's instance with mutual=False

    For creating Friend instance and marking mutual field of the followee, it will be finished automatically by the view.
    '''
    # id = models.AutoField(primary_key=True)
    followee = models.ForeignKey(User, on_delete = models.CASCADE, default=1, related_name='followee')
    follower = models.ForeignKey(User, on_delete = models.CASCADE, default=1, related_name='follower')
    mutual = models.BooleanField(default=False)             # wheater the followee followed back
    not_read = models.BooleanField(default=True)            # wheater the followee read this request