from sqlmodel import Session, select

from database.models import User
from src.models.auth_models import AuthRequest


class AuthService:
    def authentication(self, data: AuthRequest, session: Session) -> bool:
        user = session.exec(
            select(User).where(User.email == data.email)
        ).first()

        if user is not None:
            is_vip_status = user.is_vip
            print(f"[Serviço] Usuário antigo detectado: {data.email}. VIP: {is_vip_status}")
        else:
            user = User(
                email=data.email,
                name=data.name,
                provider=data.provider,
                provider_id=data.provider_id,
            )
            session.add(user)
            session.commit()
            is_vip_status = False
            print(f"[Serviço] Novo usuário registrado no banco: {data.email}")

        return is_vip_status
