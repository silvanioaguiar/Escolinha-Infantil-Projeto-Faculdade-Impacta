import flet as ft
from database import SessionLocal
import crud

def create_atividades_view(page: ft.Page):
    # --- Controles de Formulário ---
    nome_field = ft.TextField(label="Nome da Atividade")
    descricao_field = ft.TextField(label="Descrição", multiline=True)
    idade_field = ft.TextField(label="Idade Recomendada")

    # --- Tabela de Dados ---
    atividades_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Descrição")),
            ft.DataColumn(ft.Text("Idade Recomendada")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    def validar_campos():
        erros = []

        # Validação do Nome
        if not nome_field.value or not nome_field.value.strip():
            erros.append("Nome da atividade é obrigatório.")

        # Validação da Descrição
        if not descricao_field.value or not descricao_field.value.strip():
            erros.append("Descrição é obrigatória.")

        # Validação da Idade Recomendada
        if not idade_field.value or not idade_field.value.strip():
            erros.append("Idade recomendada é obrigatória.")       

        return erros

    def open_edit_dialog(atividade):
        edit_nome_field = ft.TextField(label="Nome", value=atividade.nome, width=400)       
        edit_descricao_field = ft.TextField(label="Descrição", value=atividade.descricao, width=400)
        edit_idade_recomendada_field = ft.TextField(label="Idade Recomendada", value=atividade.idade_recomendada, width=400)
        

        def close_dialog(e):
            edit_dialog.open = False
            page.update()

        def save_edit_threaded():
            try:                
                with SessionLocal() as db:
                    crud.update_atividade(
                        db=db,
                        atividade_id=atividade.id,
                        nome=edit_nome_field.value,                        
                        descricao=edit_descricao_field.value,
                        idade_recomendada=edit_idade_recomendada_field.value                       
                    )
                atividades_table.rows = load_data()
                page.update()
            except ValueError:                
                page.update()
            except Exception as ex:
                print(f"Erro ao editar a atividade: {ex}")

        def save_edit(e):
            close_dialog(e)
            page.run_thread(save_edit_threaded)

        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Atividade"),
            content=ft.Column([
                edit_nome_field,               
                edit_descricao_field,
                edit_idade_recomendada_field,               
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
            atividades = crud.get_atividades(db)
            for ativ in atividades:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(ativ.nome)),
                            ft.DataCell(ft.Text(ativ.descricao)),
                            ft.DataCell(ft.Text(ativ.idade_recomendada)),
                            ft.DataCell(ft.Row([
                                ft.IconButton(ft.Icons.EDIT, icon_color="blue", on_click=lambda e, at=ativ: open_edit_dialog(at)),
                                ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda e, at=ativ: delete_atividade(at)),
                            ])),
                        ]
                    )
                )
        return rows
    
    def fechar_alerta(e):
        page.dialog.open = False
        page.update()

    def add_atividade(e):
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
                crud.create_atividade(
                    db=db,
                    nome=nome_field.value,
                    descricao=descricao_field.value,
                    idade_recomendada=idade_field.value
                )
            for field in [nome_field, descricao_field, idade_field]:
                field.value = ""
            atividades_table.rows = load_data()
            page.update()
        except Exception as ex:
            print(f"Erro ao adicionar atividade: {ex}")

    def delete_atividade(atividade):
        with SessionLocal() as db:
            crud.delete_atividade(db, atividade.id)
        atividades_table.rows = load_data()
        page.update()

    add_button = ft.ElevatedButton("Salvar Atividade", on_click=add_atividade)

    atividades_view = ft.Column(
        controls=[
            ft.Text("Gestão de Atividades", size=30, weight=ft.FontWeight.BOLD),
            ft.Container(
                padding=ft.padding.all(10),
                bgcolor="surfacevariant",
                border_radius=ft.border_radius.all(10),
                content=ft.Column([
                    nome_field,
                    descricao_field,
                    idade_field,
                    add_button
                ])
            ),
            ft.Divider(),
            ft.Text("Atividades Cadastradas", size=20),
            ft.Container(
                height=200,
                content=ft.ListView(
                    controls=[atividades_table],
                    expand=True,
                    spacing=10,
                    padding=10,
                    auto_scroll=False
                )
            )
        ]
    )
    
    atividades_table.rows = load_data()

    return atividades_view