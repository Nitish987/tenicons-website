from .models import Profile
from random import random

# profile manager class
class ProfileManager:

    def __init__(self, user, username):
        self.profile = Profile.objects.get(user=user, username=username)

    def getUser(self):
        return self.profile.user

    def getProfile(self):
        return self.profile

    def getUniqueID(self):
        return self.profile.unique_id

    def getUsername(self):
        return self.profile.username

    def getEmail(self):
        return self.profile.email

    def isEmailVerified(self):
        return self.profile.is_email_verified

    def getProfilePicPath(self):
        return self.profile.profile_pic_path

    def getProfileCreatedDate(self):
        return self.profile.profile_create_date

    def haveRightToPost(self):
        return self.profile.right_to_post

    def haveRightToLikePost(self):
        return self.profile.right_to_like_post

    def haveRightToChangeProfilePic(self):
        return self.profile.right_to_change_profile_pic

# return the username through UUID
def get_photo_path_username(uuid):
    profile = Profile.objects.get(unique_id=uuid)
    return [profile.profile_pic_path, profile.username]

# returns true if profile exists
def profile_exists(user, username):
    return Profile.objects.filter(user=user, username=username).exists()

# creates a new profile for a user
def create_default_profile(user, username, email, is_email_verified):
    c = '1234567890'
    uniqueID = ''
    for i in range(20):
        uniqueID = uniqueID + c[int(random()*10)]

    profile = Profile(
        user=user,
        unique_id=uniqueID,
        username=username,
        email=email,
        is_email_verified=is_email_verified,
    )
    return profile

