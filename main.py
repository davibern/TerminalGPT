import openai
import config
import typer
from rich import print
from rich.table import Table


def main():

    # Configurar la API KEY
    openai.api_key = config.api_key

    # Bienvenida
    print(__welcome())

    # Mostrar ayuda
    print(__help())

    # Contexto inicial del asistente
    context = {"role": "system", "content": "Eres un asistente muy útil."}
    messages = [context]

    while True:

        # Obtengo la pregunta del usuario
        content = __prompt()
        # Si se indica nuevo se reinicia el contexto y el diálogo
        if content == "new":
            messages = [context]
            content = __prompt()
        # Mensaje de espera mientras se obtiene respuesta
        waiting = typer.style("⌛ Obteniendo respuesta...",
                              fg=typer.colors.BRIGHT_BLACK,
                              bg=typer.colors.BLACK)
        typer.echo(waiting)

        # Añado a los mensajes la pregunta del usuario
        messages.append({"role": "user", "content": content})

        # Obtengo la respuesta de la IA, concatenando los mensajes
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                messages=messages)

        # Verificar si recibo respuesta de la API
        if response.choices:
            # Se ha recibido respuesta de la API
            response_content = response.choices[0].message.content
            # Añado a los mensajes la respuesta mantener y el diálogo
            messages.append({"role": "assistant", "content": response_content})
            # Imprimo el resultado por salida estándar
            print(f"➡️ [green]{response_content}[/green]")
        else:
            # No se ha recibido ninguna respuesta de la API
            print("No se ha recibido ninguna respuesta.")


def __welcome() -> str:
    return "[bold green]Bienvenido a la Terminal de ChatGTP[/bold green]"


def __help() -> Table:
    table = Table("Comando", "Descripción")
    table.add_row("exit", "Salir de la aplicación")
    table.add_row("new", "Crear una nueva conversación")
    return table


def __prompt() -> str:
    # Obtengo la pregunta del usuario
    prompt = typer.prompt("\n💬 ¿De qué hablamos? ")

    if prompt == "exit":
        confirm = typer.confirm("🛑 ¿Estás seguro?")
        if confirm:
            print("🫡 ¡Hasta luego!")
            raise typer.Abort()

        return __prompt()

    return prompt


if __name__ == "__main__":
    typer.run(main)
