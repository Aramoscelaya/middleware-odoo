from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Sincroniza productos desde diferentes fuentes"

    def add_arguments(self, parser):
        # Argumento con valor
        parser.add_argument(
            "--provider",
            choices=["xml", "local", "api"],
            default="local",
            help="Método de carga de datos"
        )

    def handle(self, *args, **kwargs):
        provider = kwargs["provider"]
        self.stdout.write(self.style.WARNING(f"Sincronización Iniciada (CT - {provider})."))

        # Importa aquí tu lógica original
        from original_message.CT.sync_pull import run  # O tu función principal
        run(provider=provider)
        self.stdout.write(self.style.SUCCESS("Sincronización terminada."))