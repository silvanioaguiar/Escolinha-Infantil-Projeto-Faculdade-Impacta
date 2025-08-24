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

    def open_date_picker_dialog(e):
        page.open(date_picker)    

    nascimento_field_row = ft.Row([
        nascimento_display_field,
        ft.IconButton(ft.Icons.CALENDAR_MONTH, on_click=open_date_picker_dialog)
    ])
    responsavel_field = ft.TextField(label="Nome do Responsável")
    telefone_field = ft.TextField(label="Telefone do Responsável")
    endereco_field = ft.TextField(label="Endereço")

    # --- Tabela de Dados ---
    alunos_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Nascimento")),
            ft.DataColumn(ft.Text("Responsável")),
            ft.DataColumn(ft.Text("Telefone")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    def load_data():
        with SessionLocal() as db:
            alunos_table.rows.clear()
            alunos = crud.get_alunos(db)
            for aluno in alunos:
                alunos_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(aluno.nome_completo)),
                            ft.DataCell(ft.Text(aluno.data_nascimento.strftime("%d/%m/%Y"))),
                            ft.DataCell(ft.Text(aluno.nome_responsavel)),
                            ft.DataCell(ft.Text(aluno.telefone_responsavel)),
                            ft.DataCell(ft.Row([
                                ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda e, a=aluno: delete_aluno(a)),
                            ])),
                        ]
                    )
                )
        page.update()

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
            load_data()
        except Exception as ex:
            print(f"Erro ao adicionar aluno: {ex}")

    def delete_aluno(aluno):
        with SessionLocal() as db:
            crud.delete_aluno(db, aluno.id)
        load_data()

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
            ft.Row([alunos_table], scroll=ft.ScrollMode.ALWAYS)
        ]
    )
    
    # Carrega os dados iniciais
    load_data()

    return alunos_view