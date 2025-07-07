import oracledb

class DBConfig:
    @staticmethod
    def get_connection():
        try:
            conn = oracledb.connect(
                user="projectuser",
                password="StrongPass123",
                dsn="localhost/FREEPDB1"
            )
            return conn
        except oracledb.Error as e:
            print("❌ Database connection failed:", e)
            return None

    @staticmethod
    def get_lob_type():
        return oracledb.BLOB