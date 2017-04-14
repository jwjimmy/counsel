import os

os.environ["DATABASE_URL"] = "postgres://cemajazbraepnv:1e84f57cd902d0a784571a34a438e00ef3d88df1b220eed91e509106f97c2616@ec2-54-221-217-158.compute-1.amazonaws.com:5432/d2d051ft4lb9u1"
os.environ["FCM_APIKEY"] = "AAAATUa7XXE:APA91bFYsvWCAhFTjOH7OId5AvhckAPj-Rh7YxGMq_KW-gKXsxNfMEkgVrJFx5W2m2PCnUvWM6R6SNTE_m5aCxOKu-hq0wt2pyigbvAY8mV2uPqGBV8LnTIpSACvXjqZgFOw9uJ2jVh7"

from counselproj.settings import *

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'counseldev@gmail.com'
EMAIL_HOST_PASSWORD = 'poopybutthole'
EMAIL_PORT = 587
