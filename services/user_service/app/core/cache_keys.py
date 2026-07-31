class CacheKeys:
    @staticmethod
    def user(user_id: str) -> str:
        return f"user:{user_id}"

    @staticmethod
    def preferences(user_id: str) -> str:
        return f"preferences:{user_id}"