database_name = 'fsbs'


class DevelopmentConfig:
    """Development Configuration."""
    BCRYPT_LOG_ROUNDS = 4
    DB_NAME = database_name + '_development'


current_config = DevelopmentConfig
