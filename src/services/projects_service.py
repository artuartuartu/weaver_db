import json
import os
import uuid
from datetime import datetime

from sqlmodel import Session, select

from database.models import Project
from src.models.project_models import ProjectCreate, ProjectResponse

STORAGE_DIR = os.getenv("STORAGE_DIR", "./storage/projects")
os.makedirs(STORAGE_DIR, exist_ok=True)


class ProjectService:
    def create_project(self, data: ProjectCreate, session: Session) -> ProjectResponse:
        project_id = str(uuid.uuid4())
        file_name = f"{project_id}.json"
        file_path = os.path.join(STORAGE_DIR, file_name)
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M")

        initial_diagram = {"nodes": [], "edges": []}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(initial_diagram, f, ensure_ascii=False, indent=4)

        project = Project(
            id=project_id,
            name=data.name,
            file_path=file_path,
            updated_at=now_str,
            user_email=data.user_email,
        )
        session.add(project)
        session.commit()

        print(f"[ProjectService] Novo projeto '{data.name}' criado com ID {project_id}")
        return ProjectResponse(id=project_id, name=data.name, updated_at=now_str)

    def get_user_projects(self, user_email: str, session: Session) -> list[ProjectResponse]:
        projects = session.exec(
            select(Project)
            .where(Project.user_email == user_email)
            .order_by(Project.id.desc())
        ).all()

        result = [
            ProjectResponse(id=p.id, name=p.name, updated_at=p.updated_at)
            for p in projects
        ]
        print(f"[ProjectService] {len(result)} projetos encontrados para {user_email}")
        return result

    def delete_project(self, project_id: str, session: Session) -> bool:
        project = session.exec(
            select(Project).where(Project.id == project_id)
        ).first()

        if not project:
            print(f"[ProjectService] Projeto não encontrado no banco.")
            return False

        file_path = project.file_path
        project_name = project.name

        session.delete(project)
        session.commit()

        print(f"[ProjectService] Registro do projeto {project_name} removido do banco de dados.")

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"[ProjectService] Arquivo JSON deletado com sucesso: {file_path}")
        else:
            print(f"[ProjectService] Arquivo JSON não foi encontrado no caminho: {file_path}")
        return True

    def update_project_name(self, project_id: str, new_name: str, session: Session) -> ProjectResponse | None:
        project = session.exec(
            select(Project).where(Project.id == project_id)
        ).first()

        if not project:
            return None

        now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        project.name = new_name
        project.updated_at = now_str
        session.add(project)
        session.commit()
        session.refresh(project)

        print(f"[ProjectService] O projeto foi renomeado com sucesso para '{new_name}'")
        return ProjectResponse(
            id=project.id,
            name=project.name,
            updated_at=project.updated_at,
            user_email=project.user_email,
        )
