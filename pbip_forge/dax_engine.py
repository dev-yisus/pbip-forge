from typing import List
from .models import MeasureDefinition


class DAXEngine:
    """Automated generation of business DAX measures with industry standard formatting."""

    @staticmethod
    def generate_sum_measure(table_name: str, column_name: str, measure_name: str = None, is_currency: bool = False) -> MeasureDefinition:
        name = measure_name or f"Total {column_name}"
        expr = f"SUM('{table_name}'[{column_name}])"
        fmt = '"$"#,0.00' if is_currency else "#,0.00"
        return MeasureDefinition(
            name=name,
            expression=expr,
            format_string=fmt,
            description=f"Suma acumulada de {column_name} en {table_name}",
            display_folder="Métricas Base",
        )

    @staticmethod
    def generate_average_measure(table_name: str, column_name: str, measure_name: str = None, is_currency: bool = False) -> MeasureDefinition:
        name = measure_name or f"Promedio {column_name}"
        expr = f"AVERAGE('{table_name}'[{column_name}])"
        fmt = '"$"#,0.00' if is_currency else "#,0.00"
        return MeasureDefinition(
            name=name,
            expression=expr,
            format_string=fmt,
            description=f"Promedio aritmético de {column_name}",
            display_folder="Métricas Base",
        )

    @staticmethod
    def generate_count_measure(table_name: str, column_name: str, measure_name: str = None, is_distinct: bool = False) -> MeasureDefinition:
        func = "DISTINCTCOUNT" if is_distinct else "COUNT"
        prefix = "Conteo Único" if is_distinct else "Conteo"
        name = measure_name or f"{prefix} de {column_name}"
        expr = f"{func}('{table_name}'[{column_name}])"
        return MeasureDefinition(
            name=name,
            expression=expr,
            format_string="#,0",
            description=f"{prefix} de registros para {column_name}",
            display_folder="Métricas Base",
        )

    @staticmethod
    def generate_margin_ratio_measure(revenue_measure: str, cost_measure: str, measure_name: str = "Margen Bruto %") -> MeasureDefinition:
        expr = f"""DIVIDE(
    [{revenue_measure}] - [{cost_measure}],
    [{revenue_measure}],
    0
)"""
        return MeasureDefinition(
            name=measure_name,
            expression=expr,
            format_string="0.0%",
            description="Margen bruto porcentual sobre ingresos",
            display_folder="Ratios Financieros",
        )

    @staticmethod
    def generate_yoy_growth_measure(base_measure: str, date_column: str, measure_name: str = None) -> MeasureDefinition:
        name = measure_name or f"Crecimiento YoY % [{base_measure}]"
        expr = f"""VAR ValorActual = [{base_measure}]
VAR ValorAnioAnterior = CALCULATE([{base_measure}], SAMEPERIODLASTYEAR({date_column}))
RETURN
    DIVIDE(ValorActual - ValorAnioAnterior, ValorAnioAnterior, 0)"""
        return MeasureDefinition(
            name=name,
            expression=expr,
            format_string="0.0%",
            description=f"Tasa de variación interanual (Year over Year) de {base_measure}",
            display_folder="Inteligencia de Tiempo",
        )

    @staticmethod
    def generate_percent_of_total_measure(base_measure: str, table_name: str, measure_name: str = None) -> MeasureDefinition:
        name = measure_name or f"% del Total [{base_measure}]"
        expr = f"""DIVIDE(
    [{base_measure}],
    CALCULATE([{base_measure}], ALL('{table_name}')),
    0
)"""
        return MeasureDefinition(
            name=name,
            expression=expr,
            format_string="0.0%",
            description=f"Participación porcentual de {base_measure} sobre el total de {table_name}",
            display_folder="Participación y Ratios",
        )

    # Convenience Aliases
    sum_measure = generate_sum_measure
    average_measure = generate_average_measure
    count_measure = generate_count_measure
    margin_ratio_measure = generate_margin_ratio_measure
    yoy_growth_measure = generate_yoy_growth_measure
    percent_of_total_measure = generate_percent_of_total_measure

