import flet as ft
from database import SessionLocal
import crud

def create_professores_view(page: ft.Page):
    # --- Controles de Formulário ---
    nome_field = ft.TextField(label="Nome Completo")
    # cpf_field = ft.TextField(label="CPF")
    # telefone_field = ft.TextField(label="Telefone")
    cpf_field = ft.TextField(
    label="CPF",   
    on_blur=lambda e: formatar_cpf(e.control)
    )

    telefone_field = ft.TextField(
    label="Telefone",    
    on_blur=lambda e: formatar_telefone(e.control)
    )
   
    email_field = ft.TextField(label="Email")

    def formatar_cpf(field):
        digits = ''.join(filter(str.isdigit, field.value))[:11]
        formatted = ""
        if len(digits) >= 3:
            formatted += digits[:3] + "."
        if len(digits) >= 6:
            formatted += digits[3:6] + "."
        if len(digits) >= 9:
            formatted += digits[6:9] + "-"
        if len(digits) > 9:
            formatted += digits[9:]

        # Só atualiza se o valor mudou
        if field.value != formatted:
            field.value = formatted
            field.update()

    def formatar_telefone(field):
        digits = ''.join(filter(str.isdigit, field.value))[:11]
        formatted = ""
        if len(digits) >= 2:
            formatted += f"({digits[:2]}) "
        if len(digits) >= 7:
            formatted += f"{digits[2:7]}-{digits[7:]}"
        elif len(digits) > 2:
            formatted += digits[2:]

        # Só atualiza se o valor mudou
        if field.value != formatted:
            field.value = formatted
            field.update()
    
    
    def validar_campos():
        erros = []

        # Validação do nome
        if not nome_field.value.strip():
            erros.append("Nome é obrigatório.")

        # Validação do CPF (formato: 000.000.000-00)
        cpf_limpo = ''.join(filter(str.isdigit, cpf_field.value))
        if len(cpf_limpo) != 11:
            erros.append("CPF deve conter 11 dígitos.")

        # Validação do telefone (formato: (00) 00000-0000)
        telefone_limpo = ''.join(filter(str.isdigit, telefone_field.value))
        if len(telefone_limpo) < 10:
            erros.append("Telefone deve conter pelo menos 10 dígitos.")

        # Validação do email (básica)
        if "@" not in email_field.value or "." not in email_field.value:
            erros.append("Email inválido.")

        return erros

    # --- Tabela de Dados ---
    professores_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("CPF")),
            ft.DataColumn(ft.Text("Telefone")),
            ft.DataColumn(ft.Text("Email")), 
            ft.DataColumn(ft.Text("Ações")),          
        ],
        rows=[]
    )

    def open_edit_dialog(professor):
        edit_nome_field = ft.TextField(label="Nome Completo", value=professor.nome_completo, width=400)
        edit_cpf_field = ft.TextField(label="CPF", value=professor.cpf, width=400)
        edit_telefone_field = ft.TextField(label="Telefone", value=professor.telefone, width=400)
        edit_email_field = ft.TextField(label="Email", value=professor.email, width=400)
        

        def close_dialog(e):
            edit_dialog.open = False
            page.update()

        def save_edit_threaded():
            try:                
                with SessionLocal() as db:
                    crud.update_professor(
                        db=db,
                        professor_id=professor.id,
                        nome_completo=edit_nome_field.value,
                        cpf=edit_cpf_field.value,
                        telefone=edit_telefone_field.value,
                        email=edit_email_field.value,                        
                    )
                professores_table.rows = load_data()
                page.update()           
            except Exception as ex:
                print(f"Erro ao editar o professor: {ex}")

        def save_edit(e):
            close_dialog(e)
            page.run_thread(save_edit_threaded)

        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Professor"),
            content=ft.Column([
                edit_nome_field,
                edit_cpf_field,
                edit_telefone_field,
                edit_email_field,                
            ]),
            actions=[
                ft.TextButton("Salvar", on_click=save_edit),
                ft.TextButton("Cancelar", on_click=close_dialog),
            ],
        )
        page.overlay.append(edit_dialog)
        edit_dialog.open = True
        page.update()

    def load_data():
        with SessionLocal() as db:
            rows = []          
            professores = crud.get_professores(db)
            for prof in professores:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(prof.nome_completo)),
                            ft.DataCell(ft.Text(prof.cpf)),
                            ft.DataCell(ft.Text(prof.telefone)),
                            ft.DataCell(ft.Text(prof.email)),
                            ft.DataCell(ft.Row([
                                ft.IconButton(ft.Icons.EDIT, icon_color="blue", on_click=lambda e, p=prof: open_edit_dialog(p)),
                                ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda e, p=prof: delete_professor(p)),                                
                                
                            ])),
                        ]
                    )
                )
            return rows

    def fechar_alerta(e):
        page.dialog.open = False
        page.update()

    def add_professor(e):
        erros = validar_campos()
        if erros:
            alerta = ft.AlertDialog(
                title=ft.Text("Erro de Validação"),
                content=ft.Column([ft.Text(msg) for msg in erros]),
                actions=[ft.TextButton("OK", on_click=fechar_alerta)],
                modal=True
            )
            page.dialog = alerta
            page.overlay.append(alerta)
            alerta.open = True
            page.update()
            return


        try:
            with SessionLocal() as db:
                crud.create_professor(
                    db=db,
                    nome_completo=nome_field.value,
                    cpf=cpf_field.value,
                    telefone=telefone_field.value,
                    email=email_field.value
                )
            for field in [nome_field, cpf_field, telefone_field, email_field]:
                field.value = ""
                professores_table.rows = load_data()           
            page.update()
        except Exception as ex:
            print(f"Erro ao adicionar professor: {ex}")

    def delete_professor(professor):
        with SessionLocal() as db:
            crud.delete_professor(db, professor.id)
        professores_table.rows = load_data()
        page.update()

    add_button = ft.ElevatedButton("Salvar Professor", on_click=add_professor)

   
    professores_view = ft.Column(
        controls=[           
            ft.Text("Gestão de Professores", size=30, weight=ft.FontWeight.BOLD),
            ft.Container(
                padding=ft.padding.all(10),
                bgcolor="surfacevariant",
                border_radius=ft.border_radius.all(10),
                content=ft.Column([
                    nome_field,
                    cpf_field,
                    telefone_field,
                    email_field,
                    add_button
                ])
            ),
            ft.Divider(),
            ft.Text("Professores Cadastrados", size=20),            
            ft.Container(
                height=200,
                content=ft.ListView(
                    controls=[professores_table],
                    expand=True,
                    spacing=10,
                    padding=10,
                    auto_scroll=False
                )
            )
        ]
    )
    
    # Carrega os dados iniciais
    professores_table.rows = load_data()

    return professores_view