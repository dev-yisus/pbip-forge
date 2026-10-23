import json


class ThemeBuilder:
    """Generates standard Microsoft Fluent2 Power BI Report Themes."""

    @staticmethod
    def get_fluent2_theme() -> dict:
        return {
            "name": "Fluent2-CY26SU08",
            "dataColors": [
                "#115EA3",
                "#0F8387",
                "#5B5FC7",
                "#8764B8",
                "#0E700E",
                "#C239B3",
                "#004E8C",
                "#004B50",
                "#242424"
            ],
            "background": "#F5F5F5",
            "foreground": "#242424",
            "tableAccent": "#115EA3",
            "visualStyles": {
                "*": {
                    "*": {
                        "visualHeader": [
                            {"show": True}
                        ],
                        "outspacePane": [
                            {"backgroundColor": {"solid": {"color": "#FFFFFF"}}}
                        ]
                    }
                },
                "page": {
                    "*": {
                        "background": [
                            {"color": {"solid": {"color": "#F8F9FA"}}, "transparency": 0}
                        ]
                    }
                },
                "card": {
                    "*": {
                        "labels": [{"color": {"solid": {"color": "#115EA3"}}, "fontSize": 24}],
                        "categoryLabels": [{"color": {"solid": {"color": "#616161"}}, "fontSize": 10}]
                    }
                }
            }
        }
