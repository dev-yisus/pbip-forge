import json
import hashlib
from typing import List, Dict, Any
from .models import PageDefinition, VisualDefinition


class VisualBuilder:
    """Generates valid Power BI .Report visual layout definitions in JSON format."""

    @staticmethod
    def build_report_json() -> dict:
        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.0.0/schema.json",
            "themeCollection": {
                "baseTheme": {
                    "name": "Fluent2-CY26SU08",
                    "reportVersionAtImport": "5.55",
                    "type": "SharedResources"
                }
            },
            "settings": {
                "useStylingFromThemes": True
            }
        }

    @staticmethod
    def build_pages_json(pages: List[PageDefinition]) -> dict:
        pages_list = []
        for p in pages:
            page_id = VisualBuilder._slugify(p.name)
            pages_list.append({
                "name": page_id,
                "displayName": p.display_name
            })
        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
            "pageOrder": [p["name"] for p in pages_list],
            "activePageName": pages_list[0]["name"] if pages_list else "ReportSection"
        }

    @staticmethod
    def build_page_json(page: PageDefinition) -> dict:
        page_id = VisualBuilder._slugify(page.name)
        return {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/1.0.0/schema.json",
            "name": page_id,
            "displayName": page.display_name,
            "displayOption": "FitToPage",
            "width": page.width,
            "height": page.height,
            "visuals": [
                {
                    "name": f"visual_{i}",
                    "position": {
                        "x": v.x,
                        "y": v.y,
                        "width": v.width,
                        "height": v.height,
                        "z": i
                    },
                    "visual": {
                        "visualType": v.visual_type,
                        "title": {
                            "text": v.title,
                            "show": True
                        }
                    }
                }
                for i, v in enumerate(page.visuals)
            ]
        }

    @staticmethod
    def _slugify(name: str) -> str:
        clean = "".join(c for c in name if c.isalnum() or c in ("-", "_"))
        return f"ReportSection_{clean[:20]}"
