import sqlite3
from fastapi import APIRouter, HTTPException, status, Query, Depends
from src.models.project_models import ProjectCreate, ProjectResponse
from src.services.projects_service import ProjectService
from src.auth.google_auth import get_current_user_email

project_router = APIRouter(prefix="/api/projects", tags=["Projects"])
project_service = ProjectService()

@project_router.post("/create", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    name: str = Query(...),
    user_email: str = Depends(get_current_user_email)
):
    print(f"[Rota] Criando projeto '{name}' para o usuário: {user_email}")
    
    project_data = ProjectCreate(name=name, user_email=user_email)
    
    new_project = project_service.create_project(project_data)
    
    if not new_project:
        raise HTTPException(status_code=500, detail="Erro ao criar projeto no banco.")
    return new_project

@project_router.get("/users", response_model=list[ProjectResponse])
def get_user_projects(
    user_email: str = Depends(get_current_user_email) 
):
    print(f"[Rota] Buscando projetos para o e-mail autenticado: {user_email}")
    
    return project_service.get_user_projects(user_email)
    
@project_router.delete("/delete/{project_id}", status_code=status.HTTP_200_OK)
def delete_project(
    project_id: str,
    user_email: str = Depends(get_current_user_email)
):
    print(f"[Rota] Solicitação de exclusão do projeto {project_id} por: {user_email}")
    
    success = project_service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    return {"detail": "Projeto deletado com sucesso."}
    
@project_router.put("/update/{project_id}", response_model=ProjectResponse)
def update_project_name(
    project_id: str,
    new_name: str = Query(..., pattern=r"^[\w\s-]+$"),
    user_email: str = Depends(get_current_user_email) 
):
    print(f"[Rota] Renomeando projeto {project_id} para '{new_name}' por: {user_email}")
    updated_project = project_service.update_project_name(project_id, new_name)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    return updated_project