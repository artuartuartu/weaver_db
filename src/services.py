from database.connection import get_connection
from src.models import AuthRequest

class AuthService: 

    def authentication(self, data: AuthRequest) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT is_vip FROM users WHERE email = ?", (data.email,)
            )
        row = cursor.fetchone()

        if row is not None: 
            is_vip_status = bool(row[0])
            print(f"[Serviço] Usuário antigo detectado: {data.email}. VIP: {is_vip_status}")
        else:
            cursor.execute(""" 
                INSERT INTO users (email, name, provider, provider_id, is_vip)
                VALUES (?, ?, ?, ?, 0)
            """, (data.email, data.name, data.provider, data.provider_id))

            conn.commit()
            is_vip_status = False
            print(f"[Serviço] Novo usuário registrado no banco: {data.email}")
        
        conn.close()
        