import flet as ft
from database import SessionLocal
import crud
from datetime import datetime, date


def create_alunos_view(page: ft.Page):
    # --- Controles de Formulário ---
    nome_field = ft.TextField(label="Nome Completo")
    nascimento_display_field = ft.TextField(
        label="Data de Nascimento",
        read_only=True,
        icon=ft.Icons.CALENDAR_MONTH
    )

    def on_date_selected(e):
        if date_picker.value:
            nascimento_display_field.value = date_picker.value.strftime("%d/%m/%Y") 
            date_picker.visible = False           
            page.update()

    date_picker = ft.DatePicker(
        on_change=on_date_selected,
        first_date=datetime(2000, 1, 1),
        last_date=datetime.now(),        
    )   

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
    
    def open_date_picker_dialog(e):
        date_picker.visible = True
        page.open(date_picker)
        page.update()  

    nascimento_field_row = ft.Row([
        nascimento_display_field,
        ft.IconButton(ft.Icons.CALENDAR_MONTH, on_click=open_date_picker_dialog)
    ])
    responsavel_field = ft.TextField(label="Nome do Responsável")    
    endereco_field = ft.TextField(label="Endereço")

    telefone_field = ft.TextField(
        label="Telefone do Responsável",    
        on_blur=lambda e: formatar_telefone(e.control)
    )

    # --- Tabela de Dados ---
    alunos_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Nascimento")),
            ft.DataColumn(ft.Text("Responsável")),
            ft.DataColumn(ft.Text("Telefone")),
            ft.DataColumn(ft.Text("Endereço")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    def open_edit_dialog(aluno):
        edit_nome_field = ft.TextField(label="Nome Completo", value=aluno.nome_completo, width=400)
        edit_nascimento_display_field = ft.TextField(label="Data de Nascimento (dd/mm/aaaa)", value=aluno.data_nascimento.strftime("%d/%m/%Y"), width=400)
        edit_responsavel_field = ft.TextField(label="Nome do Responsável", value=aluno.nome_responsavel, width=400)
        edit_telefone_field = ft.TextField(label="Telefone do Responsável", value=aluno.telefone_responsavel, width=400)
        edit_endereco_field = ft.TextField(label="Endereço", value=aluno.endereco, width=400)

        def close_dialog(e):
            edit_dialog.open = False
            page.update()

        def save_edit_threaded():
            try:
                data_nasc = datetime.strptime(edit_nascimento_display_field.value, "%d/%m/%Y").date()
                with SessionLocal() as db:
                    crud.update_aluno(
                        db=db,
                        aluno_id=aluno.id,
                        nome_completo=edit_nome_field.value,
                        data_nascimento=data_nasc,
                        nome_responsavel=edit_responsavel_field.value,
                        telefone_responsavel=edit_telefone_field.value,
                        endereco=edit_endereco_field.value
                    )
                alunos_table.rows = load_data()
                page.update()
            except ValueError:
                edit_nascimento_display_field.error_text = "Formato de data inválido. Use dd/mm/aaaa."
                page.update()
            except Exception as ex:
                print(f"Erro ao editar aluno: {ex}")

        def save_edit(e):
            close_dialog(e)
            page.run_thread(save_edit_threaded)

        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Aluno"),
            content=ft.Column([
                edit_nome_field,
                edit_nascimento_display_field,
                edit_responsavel_field,
                edit_telefone_field,
                edit_endereco_field,
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
            alunos = crud.get_alunos(db)
            for aluno in alunos:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(aluno.nome_completo)),
                            ft.DataCell(ft.Text(aluno.data_nascimento.strftime("%d/%m/%Y"))),
                            ft.DataCell(ft.Text(aluno.nome_responsavel)),
                            ft.DataCell(ft.Text(aluno.telefone_responsavel)),
                            ft.DataCell(ft.Text(aluno.endereco)),
                            ft.DataCell(ft.Row([
                                ft.IconButton(ft.Icons.EDIT, icon_color="blue", on_click=lambda e, a=aluno: open_edit_dialog(a)),
                                ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda e, a=aluno: delete_aluno(a)),
                            ])),
                        ]
                    )
                )
            return rows

    def add_aluno(e):
        try:
            data_nasc = datetime.strptime(nascimento_display_field.value, "%d/%m/%Y").date()
            with SessionLocal() as db:
                crud.create_aluno(
                    db=db,
                    nome_completo=nome_field.value,
                    data_nascimento=data_nasc,
                    nome_responsavel=responsavel_field.value,
                    telefone_responsavel=telefone_field.value,
                    endereco=endereco_field.value
                )
            for field in [nome_field, responsavel_field, telefone_field, endereco_field]:
                field.value = ""
            nascimento_display_field.value = ""            
            alunos_table.rows = load_data()
            page.update()
        except Exception as ex:
            print(f"Erro ao adicionar aluno: {ex}")

    def delete_aluno(aluno):
        with SessionLocal() as db:
            crud.delete_aluno(db, aluno.id)
        alunos_table.rows = load_data()
        page.update()

    add_button = ft.ElevatedButton("Salvar Aluno", on_click=add_aluno)

    alunos_view = ft.Column(
        controls=[
            ft.Text("Gestão de Alunos", size=30, weight=ft.FontWeight.BOLD),
            ft.Container(
                padding=ft.padding.all(10),
                bgcolor="surfacevariant",
                border_radius=ft.border_radius.all(10),
                content=ft.Column([
                    nome_field,
                    nascimento_field_row,
                    responsavel_field,
                    telefone_field,
                    endereco_field,
                    add_button
                ])
            ),
            ft.Divider(),
            ft.Text("Alunos Cadastrados", size=20),
             ft.Container(
                height=200,
                content=ft.ListView(
                    controls=[alunos_table],
                    expand=True,
                    spacing=10,
                    padding=10,
                    auto_scroll=False
                )
            )
        ]
    )
    
    # Carrega os dados iniciais
    alunos_table.rows = load_data()

    return alunos_view