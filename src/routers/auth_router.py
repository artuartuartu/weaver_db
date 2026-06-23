from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlmodel import Session

from database.connection import get_session
from src.models.auth_models import AuthRequest, AuthResponse
from src.services.auth_service import AuthService

auth_router = APIRouter(prefix="/api/auth", tags=["Authentication"])

auth_service = AuthService()


@auth_router.post("/verify", response_model=AuthResponse)
def verify_user(data: AuthRequest, session: Session = Depends(get_session)):
    try:
        print(f"[Rota] Requisição recebida para o e-mail: {data.email}")
        is_vip = auth_service.authentication(data, session)

        return AuthResponse(
            email=data.email,
            is_vip=is_vip,
            message="Autenticação processada com sucesso na API de arquitetura limpa."
        )
    except IntegrityError as e:
        print(f"[Erro de Integridade]: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro de consistência nos dados do banco: {str(e)}"
        )
    except OperationalError as e:
        print(f"[Erro Operacional]: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="O banco de dados está temporariamente indisponível ou bloqueado."
        )
    except Exception as e:
        print(f"[Erro Desconhecido]: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno não mapeado no servidor: {str(e)}"
        )
