from .repository import backup_db, restore_db

class RespaldoService:
    
    def crear_backup(self,path=""):
        return backup_db(path)
    def restaurar_backup(self,sql_file_path):
        return restore_db(sql_file_path)
        