import flet as ft
from database import SessionLocal
import crud
from datetime import datetime

def create_cardapio_view(page: ft.Page):
    # --- Controles de Formulário --- 
    data_display_field = ft.TextField(
        label="Data",
        read_only=True,
        icon=ft.Icons.CALENDAR_MONTH
    )
    tipo_refeicao_dropdown = ft.Dropdown(
        label="Tipo de Refeição",
        options=[
            ft.dropdown.Option("Lanche da Manhã"),
            ft.dropdown.Option("Almoço"),
            ft.dropdown.Option("Lanche da Tarde"),
            ft.dropdown.Option("Jantar"),
        ]
    )
    descricao_field = ft.TextField(label="Descrição do Cardápio", multiline=True, min_lines=3)

    def on_date_selected(e):
        if date_picker.value:
            data_display_field.value = date_picker.value.strftime("%d/%m/%Y") 
            date_picker.visible = False           
            page.update()

    date_picker = ft.DatePicker(
        on_change=on_date_selected,
        first_date=datetime(2000, 1, 1),
        last_date=datetime(2099, 1, 1)        
    )  

    def open_date_picker_dialog(e):
        date_picker.visible = True
        page.open(date_picker)
        page.update()  

    data_field_row = ft.Row([
        data_display_field,
        ft.IconButton(ft.Icons.CALENDAR_MONTH, on_click=open_date_picker_dialog)
    ]) 

    def validar_campos():
        erros = []

        # Validação da data
        if not data_display_field.value.strip():
            erros.append("Data é obrigatória.")

        # Validação do tipo de refeição
        if not tipo_refeicao_dropdown.value:
            erros.append("Tipo de refeição é obrigatório.")

        # Validação da descrição
        if not descricao_field.value.strip():
            erros.append("Descrição é obrigatória.")

        return erros

    # --- Tabela de Dados ---
    cardapios_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Data")),
            ft.DataColumn(ft.Text("Tipo de Refeição")),
            ft.DataColumn(ft.Text("Descrição")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    def load_data():
        with SessionLocal() as db:
            rows = []
            cardapios = crud.get_cardapios(db)
            for item in cardapios:
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(item.data.strftime("%d/%m/%Y"))),
                            ft.DataCell(ft.Text(item.tipo_refeicao)),
                            ft.DataCell(ft.Text(item.descricao)),
                            ft.DataCell(ft.Row([
                                ft.IconButton(ft.Icons.EDIT, icon_color="blue", on_click=lambda e, i=item: open_edit_dialog(i)),
                                ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda e, i=item: delete_cardapio(i)),
                            ])),
                        ]
                    )
                )
        return rows
    
    def fechar_alerta(e):
        page.dialog.open = False
        page.update()

    def add_cardapio(e):
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
            data_cardapio = datetime.strptime(data_display_field.value, "%d/%m/%Y").date()            
            with SessionLocal() as db:
                crud.create_cardapio(
                    db=db,
                    data=data_cardapio,
                    tipo_refeicao=tipo_refeicao_dropdown.value,
                    descricao=descricao_field.value
                )
            for field in [descricao_field]:
                field.value = ""
            tipo_refeicao_dropdown.value = None
            data_display_field.value = ""  
            cardapios_table.rows = load_data()
            page.update()
        except Exception as ex:
            print(f"Erro ao adicionar cardápio: {ex}")

    def open_edit_dialog(cardapio):
        
        edit_data_display_field = ft.TextField(label="Data(dd/mm/aaaa)", value=cardapio.data.strftime("%d/%m/%Y"), width=400)
        edit_tipo_refeicao_dropdown = ft.Dropdown(
            label="Tipo de Refeição",
            value=cardapio.tipo_refeicao,
            options=[
                ft.dropdown.Option("Lanche da Manhã"),
                ft.dropdown.Option("Almoço"),
                ft.dropdown.Option("Lanche da Tarde"),
                ft.dropdown.Option("Jantar"),
            ],
            width=400
        )
        edit_descricao_field = ft.TextField(label="Descrição", value=cardapio.descricao, width=400)
        

        def close_dialog(e):
            edit_dialog.open = False
            page.update()

        def save_edit_threaded():
            try:
                data_cardapio = datetime.strptime(edit_data_display_field.value, "%d/%m/%Y").date()
                with SessionLocal() as db:
                    crud.update_cardapio(
                        db=db,  
                        cardapio_id=cardapio.id,              
                        data=data_cardapio,
                        tipo_refeicao=edit_tipo_refeicao_dropdown.value,
                        descricao=edit_descricao_field.value
                    )
                cardapios_table.rows = load_data()
                page.update()
            except ValueError:
                edit_data_display_field.error_text = "Formato de data inválido. Use dd/mm/aaaa."
                page.update()
            except Exception as ex:
                print(f"Erro ao editar o cardápio: {ex}")

        def save_edit(e):
            close_dialog(e)
            page.run_thread(save_edit_threaded)

        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Cardápio"),
            content=ft.Column([                
                edit_data_display_field,
                edit_tipo_refeicao_dropdown,
                edit_descricao_field                
            ]),
            actions=[
                ft.TextButton("Salvar", on_click=save_edit),
                ft.TextButton("Cancelar", on_click=close_dialog),
            ],
        )
        page.overlay.append(edit_dialog)
        edit_dialog.open = True
        page.update()

    def delete_cardapio(item):
        with SessionLocal() as db:
            crud.delete_cardapio(db, item.id)
        cardapios_table.rows = load_data()
        page.update()

    add_button = ft.ElevatedButton("Salvar Cardápio", on_click=add_cardapio)

    cardapio_view = ft.Column(
        controls=[
            ft.Text("Gestão de Cardápio", size=30, weight=ft.FontWeight.BOLD),
            ft.Container(
                padding=ft.padding.all(10),
                bgcolor="surfacevariant",
                border_radius=ft.border_radius.all(10),
                content=ft.Column([
                    data_field_row,
                    tipo_refeicao_dropdown,
                    descricao_field,
                    add_button
                ])
            ),
            ft.Divider(),
            ft.Text("Cardápios Cadastrados", size=20),
            ft.Container(
                height=200,
                content=ft.ListView(
                    controls=[cardapios_table],
                    expand=True,
                    spacing=10,
                    padding=10,
                    auto_scroll=False
                )
            )
        ]
    )
    
    cardapios_table.rows = load_data()

    return cardapio_view