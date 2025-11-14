import flet as ft
import unicodedata
from database import SessionLocal
import crud
from datetime import datetime, date
from sqlalchemy.orm import Session, joinedload
from models import Cardapio 





def create_agenda_view(page: ft.Page):
    with SessionLocal() as db:
        alunos = crud.get_alunos(db)
        atividades_cadastradas = crud.get_atividades(db)
        professores = crud.get_professores(db)


    # --- Caso 1: Nenhum aluno cadastrado ---
    if not alunos:
        return ft.Column(
            controls=[
                ft.Text("Agenda Diária do Aluno", size=30, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Nenhum aluno cadastrado. Por favor, vá para a tela 'Alunos' e cadastre pelo menos um aluno para poder usar a agenda.",
                    size=16
                )
            ]
        )

    # --- Caso 2: Existem alunos, montar a tela interativa ---
    selected_aluno_id = ft.Ref[int]()

      # --- Caso 3: Nenhum professor cadastrado ---
    if not professores:
        return ft.Column(
            controls=[
                ft.Text("Agenda Diária do Aluno", size=30, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Nenhum professor cadastrado. Por favor, vá para a tela de cadastros 'Professores' e cadastre pelo menos um professor para poder usar a agenda.",
                    size=16
                )
            ]
        )

    # --- Caso 4: Existem professores, montar a tela interativa ---
    selected_professor_id = ft.Ref[int]()
    
    
    # --- Controles do Formulário ---
    # lanche_manha_field1 = ft.TextField(label="Lanche da Manhã")
    # almoco_field1 = ft.TextField(label="Almoço")
    # lanche_tarde_field1 = ft.TextField(label="Lanche da Tarde")
    # jantar_field1 = ft.TextField(label="Jantar")
    cardapio_texto = ft.Text(value="", size=14, color=ft.Colors.GREEN_900 )


    
    # Date Picker
    def handle_date_change(e):
        selected_date_text.value = f"Data selecionada: {date_picker.value.strftime('%d/%m/%Y')}"

        with SessionLocal() as db:
            cardapio = buscar_cardapio_por_data(db, date_picker.value)
            print("Cardápio retornado:", cardapio)

        texto_formatado = (
            f"Lanche da Manhã: {cardapio.get('lanche_da_manha', '---')} - "
            f"Almoço: {cardapio.get('almoco', '---')} - "
            f"Lanche da Tarde: {cardapio.get('lanche_da_tarde', '---')} - "
            f"Jantar: {cardapio.get('jantar', '---')}"
        )

        cardapio_texto.value = texto_formatado
        page.update()

    def open_date_picker(e):
        page.dialog = date_picker
        date_picker.open = True
        page.update()

    date_picker = ft.DatePicker(
        on_change=handle_date_change,
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
        help_text="Selecione a data"
    )
    page.overlay.append(date_picker) # Adiciona o DatePicker à página
    selected_date_text = ft.Text()
    date_button = ft.ElevatedButton("Selecionar Data", icon=ft.Icons.CALENDAR_MONTH, on_click=open_date_picker)

    def normalizar(texto):
        return unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode().lower().replace(" ", "_")

    
    def buscar_cardapio_por_data(db: Session, data: date) -> dict:
        resultados = db.query(Cardapio).filter(Cardapio.data == data).all()
        cardapio = {normalizar(item.tipo_refeicao): item.descricao for item in resultados}
        return cardapio



    # Outros campos
    #humor_field = ft.TextField(label="Humor")
    humor_field = ft.Dropdown(
        label="Humor",
        options=[
            ft.dropdown.Option("Bom"),
            ft.dropdown.Option("Regular"),
            ft.dropdown.Option("Ruim")
        ]
    )   

    lanche_manha_field = ft.Dropdown(
        label="Lanche da Manhã",
        options=[
            ft.dropdown.Option("Ótimo - comeu tudo"),
            ft.dropdown.Option("Regular"),
            ft.dropdown.Option("Recusou")
        ]
    )

    almoco_field = ft.Dropdown(
        label="Almoço",
        options=[
            ft.dropdown.Option("Ótimo - comeu tudo"),
            ft.dropdown.Option("Regular"),
            ft.dropdown.Option("Recusou")
        ]
    )

    lanche_tarde_field = ft.Dropdown(
        label="Lanche da Tarde",
        options=[
            ft.dropdown.Option("Ótimo - comeu tudo"),
            ft.dropdown.Option("Regular"),
            ft.dropdown.Option("Recusou")
        ]
    )

    jantar_field = ft.Dropdown(
        label="Jantar",
        options=[
            ft.dropdown.Option("Ótimo - comeu tudo"),
            ft.dropdown.Option("Regular"),
            ft.dropdown.Option("Recusou")
        ]
    )

   
    sono_field = ft.TextField(label="Sonecas")
    observacoes_field = ft.TextField(label="Observações Gerais")
    
    # Atividades Checkboxes
    atividades_checkboxes = []
    for ativ in atividades_cadastradas:
        horario_inicio_field = ft.TextField(label="Horário Inicio", width=100, disabled=True)
        horario_fim_field = ft.TextField(label="Horário Fim", width=100, disabled=True)
        checkbox = ft.Checkbox(label=ativ.nome, data=ativ.id)
        
        def on_checkbox_change(e, hi=horario_inicio_field,hf=horario_fim_field):
            hi.disabled = not e.control.value
            hf.disabled = not e.control.value
            page.update()
            
        checkbox.on_change = on_checkbox_change
        atividades_checkboxes.append(ft.Row([checkbox, horario_inicio_field,horario_fim_field]))

    atividades_outras_field = ft.TextField(label="Outras Atividades (descreva aqui)", multiline=True)

    # Histórico (agora uma ListView)
    historico_list_view = ft.ListView(expand=True, spacing=10)

    # --- Lógica Principal ---

    def load_agenda_data():
        historico_list_view.controls.clear()
        if selected_aluno_id.current:
            with SessionLocal() as db:
                agendas = crud.get_agendas_por_aluno(db, selected_aluno_id.current)
                for agenda in agendas:
                    atividades_realizadas_texts = []
                    for agenda_ativ in agenda.atividades_realizadas:
                        atividade_nome = agenda_ativ.atividade.nome
                        horario = agenda_ativ.horario
                        atividades_realizadas_texts.append(ft.Text(f"- {atividade_nome} ({horario})"))
                    
                    if agenda.atividades_outras:
                        atividades_realizadas_texts.append(ft.Text(f"- Outras: {agenda.atividades_outras}"))

                    card = ft.Container(
                        padding=10,
                        border=ft.border.all(1, "outline"),
                        border_radius=5,
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"Data: {agenda.data.strftime('%d/%m/%Y')}", weight=ft.FontWeight.BOLD),
                                ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda e, a_id=agenda.id: delete_agenda_entry(a_id))
                            ]),
                            ft.Text(
                                f"Professor Responsável: {agenda.professor.nome_completo if agenda.professor else 'Não informado'}"
                            ),
                            ft.Text(f"Humor: {agenda.humor}"),
                            ft.Text(f"Sonecas: {agenda.sono}"),
                            ft.Text("Alimentação - Cardápio do Dia", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE,size=16),   
                            ft.Text(agenda.cardapio, color=ft.Colors.GREEN_900, size=14, italic=True),                         
                            ft.Row([
                                ft.Column([
                                    ft.Row([
                                      ft.Text("Lanche da Manhã:",weight=ft.FontWeight.BOLD ),
                                      ft.Text(agenda.lanche_manha),
                                    ]),

                                    ft.Row([
                                      ft.Text("Almoço:",weight=ft.FontWeight.BOLD ),
                                      ft.Text(agenda.almoco),
                                    ]),                                    
                               
                                ]),
                                 ft.Column([
                                    ft.Row([
                                      ft.Text("Lanche da Tarde:",weight=ft.FontWeight.BOLD ),
                                      ft.Text(agenda.lanche_tarde),
                                    ]),

                                    ft.Row([
                                      ft.Text("Jantar:",weight=ft.FontWeight.BOLD ),
                                      ft.Text(agenda.jantar),
                                    ]),                                  
                                ]),                             
                               
                            ]),
                     
                            ft.Text(f"Observações: {agenda.observacoes}"),
                            ft.Text("Atividades Realizadas:", weight=ft.FontWeight.BOLD,color=ft.Colors.BLUE,size=16),
                            ft.Column(atividades_realizadas_texts)
                        ])
                    )
                    historico_list_view.controls.append(card)
        page.update()

    def add_agenda_entry(e):
        if not selected_aluno_id.current or not date_picker.value:
            print("Erro: Selecione um aluno e uma data.")
            return

        atividades_selecionadas = []
        for row in atividades_checkboxes:
            checkbox = row.controls[0]
            horario_inicio_field = row.controls[1]
            horario_fim_field = row.controls[2]
            if checkbox.value:
                horario_inicio = horario_inicio_field.value or "N/A"
                horario_fim = horario_fim_field.value or "N/A"
                horario_completo = f"Das {horario_inicio} as {horario_fim}"

                atividades_selecionadas.append({
                    "atividade_id": checkbox.data,
                    "horario": horario_completo or "N/A"
                })

        with SessionLocal() as db:
            crud.create_agenda(
                db=db,
                aluno_id=selected_aluno_id.current,
                data=date_picker.value.date(),
                professor_id=selected_professor_id.current,
                humor=humor_field.value,
                # alimentacao=alimentacao_field.value,
                lanche_manha=lanche_manha_field.value,
                almoco=almoco_field.value,
                lanche_tarde=lanche_tarde_field.value,
                jantar=jantar_field.value,
                cardapio=cardapio_texto.value,
                sono=sono_field.value,
                observacoes=observacoes_field.value,
                atividades_outras=atividades_outras_field.value,
                atividades_selecionadas=atividades_selecionadas
            )
        
        # Limpar campos
        selected_date_text.value = ""
        humor_field.value = ""
        # alimentacao_field.value = ""
        lanche_manha_field.value = None
        almoco_field.value = None
        lanche_tarde_field.value = None
        jantar_field.value = None
        cardapio_texto.value = ""
        sono_field.value = ""
        observacoes_field.value = ""
        atividades_outras_field.value = ""
        for row in atividades_checkboxes:
            row.controls[0].value = False
            row.controls[1].value = ""
            row.controls[1].disabled = True

        load_agenda_data()

    def delete_agenda_entry(agenda_id):
        with SessionLocal() as db:
            crud.delete_agenda(db, agenda_id)
        load_agenda_data()

    add_button = ft.ElevatedButton("Salvar na Agenda", on_click=add_agenda_entry)

    def on_aluno_selected(e):
        selected_aluno_id.current = e.control.value
        placeholder_text.visible = False
        form_and_history.visible = True
        load_agenda_data()
        page.update()

    def on_professor_selected(e):
        selected_professor_id.current = e.control.value
        placeholder_text.visible = False
        form_and_history.visible = True
        load_agenda_data()
        page.update()

    aluno_dropdown = ft.Dropdown(
        label="Selecione um Aluno",
        options=[ft.dropdown.Option(key=aluno.id, text=aluno.nome_completo) for aluno in alunos],
        on_change=on_aluno_selected
    )

    professor_dropdown = ft.Dropdown(
        label="Professor responsável do dia",
        options=[ft.dropdown.Option(key=professor.id, text=professor.nome_completo) for professor in professores],
        on_change=on_professor_selected,
        width=300

        
    )

    
    placeholder_text = ft.Text("\nPor favor, selecione um aluno acima para ver ou adicionar lançamentos na agenda.", size=16, color=ft.Colors.GREY_700)
    
    form_and_history = ft.Column(
        visible=False,
        controls=[
            ft.Divider(),
            ft.Text("Adicionar Nova Entrada na Agenda", size=20),
            ft.Container(
                padding=ft.padding.all(10),
                bgcolor="surfacevariant",
                border_radius=ft.border_radius.all(10),
                content=ft.Column([                    
                    ft.Row([date_button, selected_date_text]),
                    professor_dropdown,
                    humor_field,
                    ft.Text("Alimentação - Cardápio do Dia:", size=16, weight=ft.FontWeight.BOLD),   
                    cardapio_texto,                     
                    ft.Row([
                        lanche_manha_field,
                        almoco_field,
                        lanche_tarde_field,
                        jantar_field
                    ], spacing=10),                   
                    sono_field,
                    observacoes_field,
                    ft.Text("Atividades Realizadas", weight=ft.FontWeight.BOLD),
                    ft.Column(atividades_checkboxes),
                    atividades_outras_field,
                    add_button
                ])
            ),
            ft.Divider(),
            ft.Text("Histórico da Agenda", size=20),
            historico_list_view
        ]
    )

    # return ft.Column(
    #     controls=[
    #         ft.Text("Agenda Diária do Aluno", size=30, weight=ft.FontWeight.BOLD),
    #         aluno_dropdown,
    #         placeholder_text,
    #         form_and_history
    #     ]
    # )
    return ft.Container(
        expand=True,
        content=ft.Column(
            scroll="auto",
            controls=[
                ft.Text("Agenda Diária do Aluno", size=30, weight=ft.FontWeight.BOLD),
                aluno_dropdown,
                placeholder_text,
                form_and_history
            ]
        )
    )
