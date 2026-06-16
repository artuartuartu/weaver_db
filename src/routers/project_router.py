import sqlite3
from fastapi import APIRouter, HTTPException, status
from src.models.project_models import ProjectCreate, ProjectResponse
from src.services.projects_service import ProjectService

project_router = APIRouter(prefix="/api/projects", tags=["Projects"])
project_service = ProjectService()

@project_router.post("/create", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate):
    try:
        print(f"[Rota] Criando novo projeto '{data.name}' para o usuário: {data.user_email}")
        return project_service.create_initial_project(data)
    except sqlite3.IntegrityError as e:
        print(f"[Erro de Integridade SQLite]: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade ao salvar o projeto. Verifique se o e-mail do usuário existe."
        )
    except Exception as e:
        print(f"[Erro Desconhecido ao criar projeto]: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno no servidor: {str(e)}"
        )

@project_router.get("/users/{user_email}", response_model=list[ProjectResponse])
def get_projects(user_email: str): 
    try:
        print(f"[Rota] Buscando projetos do usuário: {user_email}")
        return project_service.get_user_projects(user_email)
    except sqlite3.OperationalError as e:
        print(f"[Erro Operacional SQLite]: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Banco de dados travado ou inacessível."
        )
    except Exception as e:
        print(f"[Erro Desconhecido ao buscar projetos]: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno no servidor: {str(e)}"
        )
    
@project_router.delete("/delete/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, project_name: str):
    try:
        print(f"[Rota] Solicitando a exclusão do projeto: {project_name}")
        success = project_service.delete_project(project_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado para exclusão."
            )
        return None
    except Exception as e:
        print(f"[Erro ao deletar projeto]: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno no servidor: {str(e)}"
        )