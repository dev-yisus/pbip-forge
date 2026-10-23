import os
import json
import shutil
import pandas as pd
from typing import Optional, List
from .models import (
    PBIPProject,
    TableDefinition,
    ColumnDefinition,
    MeasureDefinition,
    RelationshipDefinition,
    PageDefinition,
    VisualDefinition,
    DataType,
    AggregationType,
)
from .tmdl_builder import TMDLBuilder
from .dax_engine import DAXEngine
from .theme import ThemeBuilder
from .visual_builder import VisualBuilder


class PBIPGenerator:
    """Master Orchestrator: Creates 100% valid Power BI Developer Mode (.pbip) projects."""

    def __init__(self, project: PBIPProject, output_dir: str = "."):
        self.project = project
        self.output_dir = os.path.abspath(output_dir)
        self.proj_dir = os.path.join(self.output_dir, self.project.name)
        self.report_dir = os.path.join(self.proj_dir, f"{self.project.name}.Report")
        self.model_dir = os.path.join(self.proj_dir, f"{self.project.name}.SemanticModel")

    def build(self) -> str:
        """Executes full project generation and returns root path."""
        print(f"[*] [PBIP-Forge] Generando proyecto: {self.project.name}")

        # 1. Crear directorios
        self._create_directories()

        # 2. Generar archivos raíz (.pbip)
        self._create_root_pbip()

        # 3. Generar metadatos Fabric (.platform, .pbir, .pbism)
        self._create_platform_metadata()

        # 4. Generar tema Fluent2
        self._create_theme()

        # 5. Generar TMDL (Modelo Semántico)
        self._create_tmdl_definitions()

        # 6. Generar páginas visuales y layout
        self._create_report_visuals()

        print(f"[OK] [PBIP-Forge] Proyecto generado con exito en: {self.proj_dir}")
        print(f"     Archivo para abrir: {os.path.join(self.proj_dir, f'{self.project.name}.pbip')}")
        return self.proj_dir

    def _create_directories(self):
        os.makedirs(self.proj_dir, exist_ok=True)
        os.makedirs(os.path.join(self.report_dir, ".pbi"), exist_ok=True)
        os.makedirs(os.path.join(self.report_dir, "definition", "pages"), exist_ok=True)
        os.makedirs(os.path.join(self.report_dir, "StaticResources", "SharedResources", "BaseThemes"), exist_ok=True)
        os.makedirs(os.path.join(self.model_dir, "definition", "tables"), exist_ok=True)

    def _create_root_pbip(self):
        pbip_path = os.path.join(self.proj_dir, f"{self.project.name}.pbip")
        content = {
            "version": "1.0",
            "artifacts": [
                {
                    "report": {
                        "path": f"{self.project.name}.Report"
                    }
                }
            ],
            "settings": {
                "enableAutoRecovery": True
            }
        }
        with open(pbip_path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2)

    def _create_platform_metadata(self):
        # Report .platform
        with open(os.path.join(self.report_dir, ".platform"), "w", encoding="utf-8") as f:
            f.write(json.dumps({
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
                "metadata": {
                    "type": "Report",
                    "displayName": self.project.name
                },
                "config": {
                    "version": "2.0",
                    "logicalId": "00000000-0000-0000-0000-000000000001"
                }
            }, indent=2))

        # definition.pbir
        with open(os.path.join(self.report_dir, "definition.pbir"), "w", encoding="utf-8") as f:
            json.dump({
                "version": "4.0",
                "datasetReference": {
                    "byPath": {
                        "path": f"../{self.project.name}.SemanticModel"
                    }
                }
            }, f, indent=2)

        # SemanticModel .platform
        with open(os.path.join(self.model_dir, ".platform"), "w", encoding="utf-8") as f:
            f.write(json.dumps({
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
                "metadata": {
                    "type": "SemanticModel",
                    "displayName": self.project.name
                },
                "config": {
                    "version": "2.0",
                    "logicalId": "00000000-0000-0000-0000-000000000002"
                }
            }, indent=2))

        # definition.pbism
        with open(os.path.join(self.model_dir, "definition.pbism"), "w", encoding="utf-8") as f:
            json.dump({"version": "4.2", "settings": {}}, f, indent=2)

    def _create_theme(self):
        theme_path = os.path.join(self.report_dir, "StaticResources", "SharedResources", "BaseThemes", "Fluent2-CY26SU08.json")
        with open(theme_path, "w", encoding="utf-8") as f:
            json.dump(ThemeBuilder.get_fluent2_theme(), f, indent=2)

    def _create_tmdl_definitions(self):
        # database.tmdl
        with open(os.path.join(self.model_dir, "definition", "database.tmdl"), "w", encoding="utf-8") as f:
            f.write(TMDLBuilder.build_database_tmdl(self.project.compatibility_level))

        # model.tmdl
        with open(os.path.join(self.model_dir, "definition", "model.tmdl"), "w", encoding="utf-8") as f:
            f.write(TMDLBuilder.build_model_tmdl(self.project))

        # relationships.tmdl
        if self.project.relationships:
            with open(os.path.join(self.model_dir, "definition", "relationships.tmdl"), "w", encoding="utf-8") as f:
                f.write(TMDLBuilder.build_relationships_tmdl(self.project.relationships))

        # tables/*.tmdl
        for table in self.project.tables:
            t_path = os.path.join(self.model_dir, "definition", "tables", f"{table.name}.tmdl")
            with open(t_path, "w", encoding="utf-8") as f:
                f.write(TMDLBuilder.build_table_tmdl(table))

    def _create_report_visuals(self):
        # definition/report.json
        with open(os.path.join(self.report_dir, "definition", "report.json"), "w", encoding="utf-8") as f:
            json.dump(VisualBuilder.build_report_json(), f, indent=2)

        # definition/pages/pages.json
        with open(os.path.join(self.report_dir, "definition", "pages", "pages.json"), "w", encoding="utf-8") as f:
            json.dump(VisualBuilder.build_pages_json(self.project.pages), f, indent=2)

        # Each page
        for page in self.project.pages:
            p_id = VisualBuilder._slugify(page.name)
            p_dir = os.path.join(self.report_dir, "definition", "pages", p_id)
            os.makedirs(p_dir, exist_ok=True)
            with open(os.path.join(p_dir, "page.json"), "w", encoding="utf-8") as f:
                json.dump(VisualBuilder.build_page_json(page), f, indent=2)

    @classmethod
    def from_csv(cls, csv_path: str, project_name: str, output_dir: str = ".") -> "PBIPGenerator":
        """Convenience Factory: Automatically infers schema from CSV and creates full PBIP project."""
        df = pd.read_csv(csv_path, nrows=500)
        table_name = "FactVentas"

        columns: List[ColumnDefinition] = []
        measures: List[MeasureDefinition] = []

        # Analyze columns
        for col in df.columns:
            dtype = df[col].dtype
            if pd.api.types.is_numeric_dtype(dtype):
                if pd.api.types.is_integer_dtype(dtype):
                    columns.append(ColumnDefinition(name=col, data_type=DataType.INT64, summarize_by=AggregationType.SUM))
                else:
                    columns.append(ColumnDefinition(name=col, data_type=DataType.DOUBLE, summarize_by=AggregationType.SUM, format_string="#,0.00"))
                # Auto-generate sum measure
                measures.append(DAXEngine.generate_sum_measure(table_name, col))
            elif pd.api.types.is_datetime64_any_dtype(dtype) or "fecha" in col.lower() or "date" in col.lower():
                columns.append(ColumnDefinition(name=col, data_type=DataType.DATETIME, format_string="dd/mm/yyyy"))
            else:
                columns.append(ColumnDefinition(name=col, data_type=DataType.STRING, summarize_by=AggregationType.NONE))

        # Build clean M query for CSV
        csv_abs = os.path.abspath(csv_path).replace("\\", "\\\\")
        m_query = f"""let
    Source = Csv.Document(File.Contents("{csv_abs}"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
in
    #"Promoted Headers" """

        table = TableDefinition(name=table_name, m_query=m_query, columns=columns, measures=measures)

        # Default layout page with visuals
        visuals = [
            VisualDefinition(title="Métricas Clave", visual_type="card", x=20, y=20, width=280, height=140),
            VisualDefinition(title="Análisis de Rendimiento", visual_type="clusteredColumnChart", x=320, y=20, width=920, height=360),
            VisualDefinition(title="Tabla Detalle de Transacciones", visual_type="tableEx", x=20, y=400, width=1220, height=300),
        ]
        page = PageDefinition(name="ResumenEjecutivo", display_name="Resumen Ejecutivo", visuals=visuals)

        project = PBIPProject(name=project_name, tables=[table], pages=[page])
        return cls(project, output_dir=output_dir)
