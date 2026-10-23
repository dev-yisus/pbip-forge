import os
import sys

# Ensure library is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pbip_forge import (
    PBIPGenerator,
    PBIPProject,
    TableDefinition,
    ColumnDefinition,
    DataType,
    AggregationType,
    PageDefinition,
    VisualDefinition,
)
from pbip_forge.dax_engine import DAXEngine


def run_demo(output_dir: str = "./demo_output"):
    csv_file = os.path.join(os.path.dirname(__file__), "sample_superstore.csv")
    csv_abs = os.path.abspath(csv_file).replace("\\", "\\\\")

    project_name = "SuperStore_Executive_Dashboard"

    # 1. Definir columnas
    columns = [
        ColumnDefinition("ID_Venta", DataType.INT64, summarize_by=AggregationType.NONE),
        ColumnDefinition("Fecha", DataType.DATETIME, format_string="yyyy-mm-dd"),
        ColumnDefinition("Region", DataType.STRING),
        ColumnDefinition("Categoria", DataType.STRING),
        ColumnDefinition("Subcategoria", DataType.STRING),
        ColumnDefinition("Cliente", DataType.STRING),
        ColumnDefinition("Cantidad", DataType.INT64, summarize_by=AggregationType.SUM),
        ColumnDefinition("Precio_Unitario", DataType.DOUBLE, format_string='"$"#,0.00', summarize_by=AggregationType.AVERAGE),
        ColumnDefinition("Total_Venta", DataType.DOUBLE, format_string='"$"#,0.00', summarize_by=AggregationType.SUM),
        ColumnDefinition("Costo_Total", DataType.DOUBLE, format_string='"$"#,0.00', summarize_by=AggregationType.SUM),
    ]

    # 2. Generar medidas DAX automáticas
    measures = [
        DAXEngine.generate_sum_measure("Ventas", "Total_Venta", "Ingresos Totales", is_currency=True),
        DAXEngine.generate_sum_measure("Ventas", "Costo_Total", "Costo Total", is_currency=True),
        DAXEngine.generate_average_measure("Ventas", "Total_Venta", "Ticket Promedio", is_currency=True),
        DAXEngine.generate_count_measure("Ventas", "Cliente", "Total Clientes Únicos", is_distinct=True),
        DAXEngine.generate_margin_ratio_measure("Ingresos Totales", "Costo Total", "Margen Bruto %"),
    ]

    # 3. Query M de Power Query
    m_query = f"""let
    Source = Csv.Document(File.Contents("{csv_abs}"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
    #"Promoted Headers" """

    table = TableDefinition(name="Ventas", m_query=m_query, columns=columns, measures=measures)

    # 4. Diseñar visuales de la página
    visuals = [
        VisualDefinition(title="Ingresos Totales", visual_type="card", x=20, y=20, width=280, height=130),
        VisualDefinition(title="Margen Bruto %", visual_type="card", x=320, y=20, width=280, height=130),
        VisualDefinition(title="Clientes Únicos", visual_type="card", x=620, y=20, width=280, height=130),
        VisualDefinition(title="Ventas por Región", visual_type="clusteredColumnChart", x=20, y=170, width=580, height=320),
        VisualDefinition(title="Ventas por Categoría", visual_type="donutChart", x=620, y=170, width=580, height=320),
        VisualDefinition(title="Detalle General", visual_type="tableEx", x=20, y=510, width=1180, height=190),
    ]
    page = PageDefinition(name="ResumenGeneral", display_name="Resumen General", visuals=visuals)

    project = PBIPProject(name=project_name, tables=[table], pages=[page])

    # 5. Generar proyecto
    generator = PBIPGenerator(project, output_dir=output_dir)
    return generator.build()


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "demo_output")
    res = run_demo(out)
    pbip_full = os.path.join(res, "SuperStore_Executive_Dashboard.pbip")
    print(f"\n[EXITO] Demo completada con exito!")
    print(f"        Archivo PBIP listo para abrir en Power BI Desktop: {pbip_full}")

