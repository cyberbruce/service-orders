from django.apps import AppConfig
from django.db.backends.signals import connection_created




def activate_foreign_keys(sender, connection, **kwargs):
    """Enable foreign key constraints on SQLite."""
    if connection.vendor == "sqlite":
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("PRAGMA journal_mode = WAL;")         
        cursor.close()
        # print("SQLITE - pragma foreign keys ON and journal mode WAL")



class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"
    
    
    def ready(self):
        connection_created.connect(activate_foreign_keys)
        
    