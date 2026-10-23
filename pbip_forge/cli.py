import argparse
import sys
import os
from .generator import PBIPGenerator


def main():
    parser = argparse.ArgumentParser(
        prog="pbip-forge",
        description="PBIP-Forge: Reverse-Engineered Power BI Project Generator (.pbip, TMDL, DAX)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")

    # Command: build
    build_parser = subparsers.add_parser("build", help="Construye un proyecto PBIP desde un archivo de datos")
    build_parser.add_argument("--input", "-i", required=True, help="Ruta al archivo CSV de datos")
    build_parser.add_argument("--name", "-n", default="PBIP_Analytics_Project", help="Nombre del proyecto Power BI")
    build_parser.add_argument("--output", "-o", default=".", help="Directorio destino")

    # Command: demo
    demo_parser = subparsers.add_parser("demo", help="Genera un proyecto PBIP de demostración funcional")
    demo_parser.add_argument("--output", "-o", default="./demo_output", help="Directorio destino para la demo")

    args = parser.parse_args()

    if args.command == "build":
        if not os.path.exists(args.input):
            print(f"❌ Error: El archivo no existe: {args.input}")
            sys.exit(1)
        generator = PBIPGenerator.from_csv(args.input, project_name=args.name, output_dir=args.output)
        generator.build()

    elif args.command == "demo":
        from ..examples.quick_start_demo import run_demo
        run_demo(args.output)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
