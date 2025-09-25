import flet as ft
import database
import models
from views import alunos_view
from views import professores_view


try:
    models.Base.metadata.create_all(bind=database.engine)
    print("Tabelas criadas com sucesso (se não existiam)!")
except Exception as e:
    print(f"Erro ao conectar ou criar tabelas: {e}")

def main(page: ft.Page):
    page.title = "Sistema da Escolinha Infantil"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def route_change(route):
         # Evita duplicação de views
        if page.views and page.views[-1].route == page.route:
            return  

        if page.route == "/":
            page.views.clear()  
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Text("Bem-vindo ao Sistema da Escolinha!", size=30),
                        ft.Row(
                            [   
                                ft.TextButton(
                                content=ft.Row([
                                    ft.Icon(name=ft.Icons.BOOK),
                                    ft.Text("Agenda")
                                ]),                           
                                ),

                                ft.TextButton(
                                content=ft.Row([
                                    ft.Icon(name=ft.Icons.APP_REGISTRATION),
                                    ft.Text("Cadastros")
                                ]),
                                on_click=lambda _: page.go("/cadastros")),

                            
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )
        elif page.route == "/agenda":
            page.views.append(
                ft.View(
                    "/agenda",
                    [
                        ft.AppBar(title=ft.Text("Agenda"), bgcolor=ft.Colors.ON_SURFACE_VARIANT),
                        agenda_view.create_agenda_view(page)
                    ]
                )
            )
        elif page.route == "/cadastros":
            page.views.append(
                ft.View(
                    "/cadastros",
                    [
                        ft.AppBar(title=ft.Text("Cadastros", color=ft.Colors.WHITE), bgcolor=ft.Colors.ON_SURFACE_VARIANT),
                        ft.ElevatedButton("Alunos", on_click=lambda _: page.go("/cadastros/alunos")),
                        ft.ElevatedButton("Professores", on_click=lambda _: page.go("/cadastros/professores")),
                        ft.ElevatedButton("Atividades"),
                        ft.ElevatedButton("Cardápio"),
                    ],
                )
            )
        elif page.route == "/cadastros/alunos":
            page.views.append(
                ft.View(
                    "/cadastros/alunos",
                    [
                        ft.AppBar(title=ft.Text("Cadastro de Alunos",color=ft.Colors.WHITE), bgcolor=ft.Colors.ON_SURFACE_VARIANT),
                        alunos_view.create_alunos_view(page)
                    ]
                )
            )
        elif page.route == "/cadastros/professores":
            page.views.append(
                ft.View(
                    "/cadastros/professores",
                    [
                        ft.AppBar(title=ft.Text("Cadastro de Professores", color=ft.Colors.WHITE), bgcolor=ft.Colors.ON_SURFACE_VARIANT),
                        professores_view.create_professores_view(page)
                    ]
                )
            )
    
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)