from typing import List
from .models import TableDefinition, RelationshipDefinition, PBIPProject, DataType


class TMDLBuilder:
    """Serializes project definitions into valid Microsoft Tabular Model Definition Language (TMDL)."""

    @staticmethod
    def build_database_tmdl(compatibility_level: int = 1600) -> str:
        return f"database\n\tcompatibilityLevel: {compatibility_level}\n\n"

    @staticmethod
    def build_model_tmdl(project: PBIPProject) -> str:
        lines = [
            "model Model",
            f"\tculture: {project.culture}",
            "\tdefaultPowerBIDataSourceVersion: powerBI_V3",
            "\tsourceQueryCulture: es-PE",
            "\tdataAccessOptions",
            "\t\tlegacyRedirects",
            "\t\treturnErrorValuesAsNull",
            "",
            "\tannotation PBI_QueryOrder = " + str([t.name for t in project.tables]),
            "\tannotation __PBI_TimeIntelligenceEnabled = 0",
            "\tannotation PBIDesktopVersion = 2.138.1452.0 (24.11)",
            "\tannotation PBI_ProTooling = [\"DevMode\"]",
            "",
        ]

        # References to tables
        for table in project.tables:
            lines.append(f"\tref table {table.name}")

        lines.append("")
        return "\n".join(lines)

    @staticmethod
    def build_relationships_tmdl(relationships: List[RelationshipDefinition]) -> str:
        if not relationships:
            return ""

        lines = []
        for r in relationships:
            active_str = "" if r.is_active else "\n\tisActive: false"
            cross_filter = "" if r.cross_filtering == "single" else f"\n\tcrossFilteringBehavior: {r.cross_filtering}"
            lines.append(
                f"relationship '{r.from_table}_{r.from_column}_to_{r.to_table}_{r.to_column}'\n"
                f"\tfromColumn: {r.from_table}.{r.from_column}\n"
                f"\ttoColumn: {r.to_table}.{r.to_column}"
                f"{active_str}"
                f"{cross_filter}\n"
            )
        return "\n".join(lines)

    @staticmethod
    def build_table_tmdl(table: TableDefinition) -> str:
        lines = [
            f"table {table.name}",
            f"\tlineageTag: {TMDLBuilder._uuid_hash(table.name)}",
        ]

        # Measures
        for m in table.measures:
            lines.append("")
            lines.append(f"\tmeasure '{m.name}' =")
            # Multiline DAX indentation
            for expr_line in m.expression.strip().split("\n"):
                lines.append(f"\t\t{expr_line}")
            if m.format_string:
                lines.append(f"\t\tformatString: {m.format_string}")
            lines.append(f"\t\tlineageTag: {TMDLBuilder._uuid_hash(table.name + '_' + m.name)}")
            if m.display_folder:
                lines.append(f"\t\tdisplayFolder: \"{m.display_folder}\"")
            if m.description:
                lines.append(f"\t\tdescription: \"{m.description}\"")

        # Columns
        for c in table.columns:
            lines.append("")
            lines.append(f"\tcolumn {c.name}")
            lines.append(f"\t\tdataType: {c.data_type.value}")
            if c.format_string:
                lines.append(f"\t\tformatString: {c.format_string}")
            lines.append(f"\t\tlineageTag: {TMDLBuilder._uuid_hash(table.name + '_' + c.name)}")
            lines.append(f"\t\tsummarizeBy: {c.summarize_by.value}")
            lines.append(f"\t\tsourceColumn: {c.source_column}")
            if c.is_hidden:
                lines.append("\t\tisHidden")
            lines.append(f'\t\tannotation SummarizationSetBy = Automatic')

        # Partition with Power Query M Expression
        lines.append("")
        lines.append(f"\tpartition {table.name} = m")
        lines.append("\t\tmode: import")
        lines.append("\t\tsource =")
        
        # Format M query with double tabs
        for m_line in table.m_query.strip().split("\n"):
            lines.append(f"\t\t\t{m_line}")

        lines.append("")
        return "\n".join(lines)

    @staticmethod
    def _uuid_hash(val: str) -> str:
        """Deterministic pseudo-UUID for TMDL lineageTag."""
        import hashlib
        h = hashlib.md5(val.encode("utf-8")).hexdigest()
        return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"

    # Alias
    serialize_table = build_table_tmdl

