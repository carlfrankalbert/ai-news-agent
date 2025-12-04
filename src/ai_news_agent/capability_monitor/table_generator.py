"""Generate markdown capability table from data."""

from typing import Dict
from datetime import datetime
from .config import MODELS, CAPABILITIES, SYMBOLS


class TableGenerator:
    """Generates markdown capability comparison tables."""

    def __init__(self):
        """Initialize table generator."""
        self.symbols = SYMBOLS

    def generate_table(self, capabilities: Dict[str, Dict]) -> str:
        """
        Generate markdown table from capability data.
        
        Args:
            capabilities: Dictionary of model capabilities
            
        Returns:
            Markdown formatted table string
        """
        lines = []
        
        # Header
        header = "| Capability | " + " | ".join(MODELS) + " |"
        lines.append(header)
        
        # Separator
        separator = "|---|" + "|".join([":---:" for _ in MODELS]) + "|"
        lines.append(separator)
        
        # Category rows
        for category, cap_list in CAPABILITIES.items():
            # Category header row
            category_row = f"| **{category}** | " + " | ".join(["" for _ in MODELS]) + " |"
            lines.append(category_row)
            
            # Capability rows
            for capability in cap_list:
                row_values = []
                for model in MODELS:
                    model_caps = capabilities.get(model, {}).get("capabilities", {})
                    category_caps = model_caps.get(category, {})
                    value = category_caps.get(capability, self.symbols["not_supported"])
                    row_values.append(value)
                
                row = f"| {capability} | " + " | ".join(row_values) + " |"
                lines.append(row)
        
        return "\n".join(lines)

    def generate_full_report(
        self, 
        capabilities: Dict[str, Dict], 
        changes: list = None
    ) -> str:
        """
        Generate full markdown report with table and metadata.
        
        Args:
            capabilities: Dictionary of model capabilities
            changes: List of change descriptions
            
        Returns:
            Complete markdown report
        """
        lines = []
        
        # Title
        lines.append("# AI Model Capability Comparison")
        lines.append("")
        lines.append(f"*Last updated: {datetime.now().strftime('%Y-%m-%d')}*")
        lines.append("")
        
        # Table
        lines.append(self.generate_table(capabilities))
        lines.append("")
        
        # Legend
        lines.append("### Legend")
        lines.append("")
        lines.append(f"- `{self.symbols['supported']}` = Supported")
        lines.append(f"- `{self.symbols['not_supported']}` = Not supported")
        lines.append(f"- `{self.symbols['partial']}` = Partial support")
        lines.append(f"- `{self.symbols['best']}` = Best in category (only ONE model per row can have this)")
        lines.append("")
        
        # Sources
        lines.append("### Sources")
        lines.append("")
        sources_set = set()
        for model, data in capabilities.items():
            model_sources = data.get("sources", [])
            sources_set.update(model_sources)
        
        for source in sorted(sources_set):
            lines.append(f"- {source}")
        lines.append("")
        
        # Changes section
        if changes:
            lines.append("### Changes from Previous Update")
            lines.append("")
            for change in changes:
                lines.append(f"- {change}")
            lines.append("")
        
        return "\n".join(lines)

    def save_table(self, capabilities: Dict[str, Dict], filepath: str):
        """
        Save table to file.
        
        Args:
            capabilities: Dictionary of model capabilities
            filepath: Path to save file
        """
        table = self.generate_table(capabilities)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(table)

    def save_report(
        self, 
        capabilities: Dict[str, Dict], 
        filepath: str, 
        changes: list = None
    ):
        """
        Save full report to file.
        
        Args:
            capabilities: Dictionary of model capabilities
            filepath: Path to save file
            changes: List of change descriptions
        """
        report = self.generate_full_report(capabilities, changes)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)

