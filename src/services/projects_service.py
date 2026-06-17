import os
import json
import uuid
from datetime import datetime
from database.connection import get_connection
from src.models.project_models import ProjectCreate, ProjectResponse 

STORAGE_DIR = "./storage/projects"
os.makedirs(STORAGE_DIR, exist_ok=True)

class ProjectService:
    def create_project(self, data: ProjectCreate) -> ProjectResponse:
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
    
    def delete_project(self, project_id: str) -> bool:
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT file_path, name FROM projects WHERE id = ?", (project_id,))
            row = cursor.fetchone()

            if not row:
                print(f"[ProjectService] Projeto {project_name} não encontrado no banco.")
                conn.close()
                return False
            
            file_path = row[0]
            project_name = row[1]

            cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            conn.commit()
            conn.close()
            print(f"[ProjectService] Registro do projeto {project_name} removido do banco de dados.")

            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"[ProjectService] Arquivo JSON deletado com sucesso: {file_path}")
            else:
                print(f"[ProjectService] Arquivo JSON não foi encontrado no caminho: {file_path}")
            return True
        except Exception as e:
            print(f"[ProjectService] Erro ao deletar projeto {project_name}: {str(e)}")
            try:
                conn.close()
            except:
                pass
            raise e
        
    def update_project_name(self, project_id: str, new_name: str) -> ProjectResponse | None:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            now_str = datetime.now().strftime("%d/%m/%Y %H:%M")

            cursor.execute("""
                UPDATE projects
                SET name = ?, updated_at = ?
                WHERE id = ?
            """, (new_name, now_str, project_id))

            conn.commit()

            cursor.execute("SELECT id, name, updated_at, user_email FROM projects WHERE id = ?", (project_id,))
            row = cursor.fetchone()
            conn.close()

            if row:
                print(f"[ProjectService] O projeto foi renomeado com sucesso para '{new_name}'")
                return ProjectResponse(id=row[0], name=row[1], updated_at=row[2], user_email=row[3])
            return None
        
        except Exception as e:
            print(f"[ProjectService] Erro ao renomear projeto {project_id}: {str(e)}")
            try: conn.close()
            except: pass
            raise e
