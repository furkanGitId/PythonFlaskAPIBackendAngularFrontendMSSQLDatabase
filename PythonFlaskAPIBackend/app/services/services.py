from app.helpers.db_connection import get_db_connection, row_to_dict

class LoginService:
    @staticmethod
    def validate_user(username, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("select COUNT(1) from logins where username = ? AND password = ?", (username, password))
        count = cursor.fetchone()[0]
        if count > 0:
            return True
        return False

class UserService: 
    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("EXEC dbo.sp_get_all_users")
        
        rows = cursor.fetchall()
        
        # Convert list of rows to list of dicts
        results = [row_to_dict(cursor, row) for row in rows]
        
        conn.close()
        return results

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("EXEC dbo.sp_get_user_by_id @UserId = ?", (user_id,))
        
        row = cursor.fetchone()
        result = row_to_dict(cursor, row) if row else None
        
        conn.close()
        return result

    @staticmethod
    def create_user(name, email):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("EXEC dbo.sp_create_user @Name = ?, @Email = ?", (name, email))
        conn.commit() # Important: Commit changes!
        conn.close()     
        return {"name": name, "email": email}

    @staticmethod
    def update_user(user_id, name, email):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("EXEC dbo.sp_update_user @UserId = ?, @Name = ?, @Email = ?", (user_id, name, email))
        updated_row = cursor.fetchone()
        updated_user = row_to_dict(cursor, updated_row) if updated_row else None
        conn.commit()
        conn.close()
        return updated_user

    @staticmethod
    def delete_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("EXEC dbo.sp_delete_user @UserId = ?", (user_id,))
        rows_affected = cursor.fetchone()[0]  # @@ROWCOUNT returned
        conn.commit()
        conn.close()
        return rows_affected > 0