import os
import json
import uuid
from datetime import datetime
from database.connection import get_connection
from src.models.project_models import ProjectCreate, ProjectResponse 

STORAGE_DIR = "./storage/projects"
os.makedirs(STORAGE_DIR, exist_ok=True)

class ProjectService:
    def create_initial_project(self, data: ProjectCreate) -> ProjectResponse:
        project_id = str(uuid.uuid4())
        file_name = f"{project_id}.json"
        file_path = os.path.join(STORAGE_DIR, file_name)
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M")

        initial_diagram = {
            "nodes": [],
            "edges": []
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(initial_diagram, f, ensure_ascii=False, indent=4)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO projects (id, name, file_path, updated_at, user_email)
            VALUES (?, ?, ?, ?, ?)           
        """, (project_id, data.name, file_path, now_str, data.user_email))

        conn.commit()
        conn.close()

        print(f"[ProjectService] Novo projeto '{data.name}' criado com ID {project_id}")
        return ProjectResponse(id=project_id, name=data.name, updated_at=now_str)
    
    def get_user_projects(self, user_email: str) -> list[ProjectResponse]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, updated_at
            FROM projects
            WHERE user_email = ?
            ORDER BY id DESC
        """, (user_email,))

        rows = cursor.fetchall()
        conn.close()

        projects = []
        for row in rows:
            projects.append(
                ProjectResponse(
                    id=row[0],
                    name=row[1],
                    updated_at=row[2]
                )
            )
        print(f"[ProjectService] {len(projects)} projetos encontrados para {user_email}")
        return projects