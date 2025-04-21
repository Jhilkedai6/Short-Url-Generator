# from sqlalchemy.orm import Session
# from modle import Url
# from redis import Redis


# redis_medium = None

# def startup():
#     global redis_medium

#     if redis_medium is None:
#         redis_medium = Redis(host="localhost", port=6379)

#     return redis_medium


# def shutdown():
#     global redis_medium

#     if redis_medium:
#         redis_medium.close()
#         redis_medium = None
