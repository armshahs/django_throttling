from rest_framework.throttling import UserRateThrottle


class post_todo_generics_throttle(UserRateThrottle):
    scope = "todo-post"
