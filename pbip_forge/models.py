from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


class DataType(str, Enum):
    STRING = "string"
    INT64 = "int64"
    DOUBLE = "double"
    DECIMAL = "decimal"
    DATETIME = "dateTime"
    BOOLEAN = "boolean"


class AggregationType(str, Enum):
    NONE = "none"
    SUM = "sum"
    COUNT = "count"
    AVERAGE = "average"
    MIN = "min"
    MAX = "max"
    DISTINCT_COUNT = "distinctCount"


@dataclass
class ColumnDefinition:
    name: str
    data_type: DataType = DataType.STRING
    source_column: Optional[str] = None
    format_string: Optional[str] = None
    summarize_by: AggregationType = AggregationType.NONE
    is_hidden: bool = False
    description: Optional[str] = None

    def __post_init__(self):
        if not self.source_column:
            self.source_column = self.name


@dataclass
class MeasureDefinition:
    name: str
    expression: str
    format_string: Optional[str] = None
    description: Optional[str] = None
    display_folder: Optional[str] = None


@dataclass
class RelationshipDefinition:
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    cardinality: str = "manyToOne"  # manyToOne, oneToOne, oneToMany, manyToMany
    cross_filtering: str = "single"  # single, bothDirections
    is_active: bool = True


@dataclass
class TableDefinition:
    name: str
    m_query: str = '#table({}, {})'
    columns: List[ColumnDefinition] = field(default_factory=list)
    measures: List[MeasureDefinition] = field(default_factory=list)
    description: Optional[str] = None
    is_date_table: bool = False



@dataclass
class VisualDefinition:
    title: str
    visual_type: str  # card, clusteredColumnChart, lineChart, donutChart, tableEx, pivotTable
    x: int
    y: int
    width: int
    height: int
    fields: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PageDefinition:
    name: str
    display_name: str
    visuals: List[VisualDefinition] = field(default_factory=list)
    width: int = 1280
    height: int = 720


@dataclass
class PBIPProject:
    name: str
    compatibility_level: int = 1600
    culture: str = "es-ES"
    tables: List[TableDefinition] = field(default_factory=list)
    relationships: List[RelationshipDefinition] = field(default_factory=list)
    pages: List[PageDefinition] = field(default_factory=list)
