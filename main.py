import openai
import config
import typer
from rich import print
from rich.table import Table


def main():

    # Configurar la API KEY
    openai.api_key = config.api_key
    
    # Saludo inicial del programa
    print("[bold green]TerminalGPT [DAVIBERN][/bold green]")
    
    # Mostrar ayuda inicial
    table = Table("Comando", "Descripción")
    table.add_row("exit", "Salir de la aplicación")
    table.add_row("new", "Crear una nueva conversación")

    print(table)

    # Contexto inicial del asistente
    context = {"role": "system", "content": "Eres un asistente muy útil."}
    messages = [context]

    while True:

        # Obtengo la pregunta del usuario
        content = __prompt()
        
        if  content == "new":
            messages = [context]
            content = __prompt()

        # Añado a los mensajes la pregunta del usuario
        messages.append({"role": "user", "content": content})

        # Obtengo la respuesta de la IA, concatenando los mensajes
        response = openai.ChatCompletion.create(model = "gpt-3.5-turbo",
                                                messages = messages)
        
        response_content = response.choices[0].message.content
        
        # Añado a los mensajes la respuesta de la IA para mantener el contexto y el diálogo
        messages.append({"role": "assistant", "content": response_content})

        # Imprimo el resultado por salida estándar
        print(f"➡️ [green]{response_content}[/green]")


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