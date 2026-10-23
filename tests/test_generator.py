"""
Tests unitarios para pbip-forge.
Verifica la generacion de TMDL, DAX, modelos y estructura PBIP completa.
"""

import os
import shutil
import tempfile
import unittest

from pbip_forge.models import (
    PBIPProject,
    TableDefinition,
    ColumnDefinition,
    MeasureDefinition,
    DataType,
)
from pbip_forge.tmdl_builder import TMDLBuilder
from pbip_forge.dax_engine import DAXEngine
from pbip_forge.generator import PBIPGenerator


class TestPBIPForge(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_tmdl_builder(self):
        table = TableDefinition(
            name="Ventas",
            columns=[
                ColumnDefinition(name="ID", data_type=DataType.INT64),
                ColumnDefinition(name="Monto", data_type=DataType.DECIMAL),
            ],
            measures=[
                MeasureDefinition(name="Total", expression="SUM('Ventas'[Monto])", format_string="$#,0.00")
            ]
        )
        tmdl = TMDLBuilder.serialize_table(table)
        self.assertIn("table Ventas", tmdl)
        self.assertIn("column ID", tmdl)
        self.assertIn("dataType: int64", tmdl)
        self.assertIn("measure 'Total' =", tmdl)
        self.assertIn("SUM('Ventas'[Monto])", tmdl)

    def test_dax_engine(self):
        m_sum = DAXEngine.sum_measure("Ventas", "Monto", "Monto Total")
        self.assertEqual(m_sum.name, "Monto Total")
        self.assertIn("SUM('Ventas'[Monto])", m_sum.expression)

        m_ratio = DAXEngine.margin_ratio_measure("Ingresos", "Costos", "Margen")
        self.assertEqual(m_ratio.name, "Margen")
        self.assertIn("DIVIDE(", m_ratio.expression)
        self.assertEqual(m_ratio.format_string, "0.0%")

    def test_full_project_generation(self):
        table = TableDefinition(
            name="Productos",
            columns=[
                ColumnDefinition(name="Cod", data_type=DataType.STRING),
                ColumnDefinition(name="Precio", data_type=DataType.DECIMAL),
            ],
            measures=[
                DAXEngine.sum_measure("Productos", "Precio", "Suma Precios")
            ]
        )
        project = PBIPProject(name="TestProject", tables=[table])
        generator = PBIPGenerator(project, output_dir=self.temp_dir)
        proj_dir = generator.build()

        # Comprobar existencia de archivos principales
        pbip_file = os.path.join(proj_dir, "TestProject.pbip")
        self.assertTrue(os.path.isfile(pbip_file))

        sem_dir = os.path.join(proj_dir, "TestProject.SemanticModel")
        self.assertTrue(os.path.isdir(sem_dir))
        self.assertTrue(os.path.isfile(os.path.join(sem_dir, "definition", "database.tmdl")))
        self.assertTrue(os.path.isfile(os.path.join(sem_dir, "definition", "model.tmdl")))
        self.assertTrue(os.path.isfile(os.path.join(sem_dir, "definition", "tables", "Productos.tmdl")))

        rep_dir = os.path.join(proj_dir, "TestProject.Report")
        self.assertTrue(os.path.isdir(rep_dir))
        self.assertTrue(os.path.isfile(os.path.join(rep_dir, "definition.pbir")))
        self.assertTrue(os.path.isfile(os.path.join(rep_dir, "definition", "report.json")))


if __name__ == "__main__":
    unittest.main()
