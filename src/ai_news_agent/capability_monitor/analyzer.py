"""Analyze and merge capability data with benchmark results."""

from typing import Dict, List
from .config import MODELS, CAPABILITIES, SYMBOLS


class CapabilityAnalyzer:
    """Analyzes and processes capability data."""

    def __init__(self):
        """Initialize analyzer."""
        self.symbols = SYMBOLS

    def merge_with_benchmarks(
        self, 
        capabilities: Dict[str, Dict], 
        benchmarks: Dict[str, str]
    ) -> Dict[str, Dict]:
        """
        Merge capability data with benchmark results to assign ⭐.
        
        Args:
            capabilities: Dictionary of model capabilities
            benchmarks: Dictionary mapping capability to best model
            
        Returns:
            Updated capabilities with ⭐ assignments
        """
        merged = {}
        
        for model, data in capabilities.items():
            merged[model] = data.copy()
            model_capabilities = merged[model].get("capabilities", {})
            
            # Apply benchmark results (⭐ for best-in-category)
            for category, caps in model_capabilities.items():
                for cap_name, cap_value in caps.items():
                    # Check if this model is best in this category
                    best_model = benchmarks.get(cap_name)
                    if best_model and model in best_model:
                        # Replace with ⭐ (only if currently ✔︎ or ~)
                        if cap_value in [self.symbols["supported"], self.symbols["partial"]]:
                            model_capabilities[category][cap_name] = self.symbols["best"]
        
        return merged

    def compare_with_previous(
        self, 
        current: Dict[str, Dict], 
        previous: Dict[str, Dict]
    ) -> List[str]:
        """
        Compare current capabilities with previous to generate change report.
        
        Args:
            current: Current capability data
            previous: Previous capability data
            
        Returns:
            List of change descriptions
        """
        changes = []
        
        if not previous:
            return ["Initial capability table created."]
        
        for model in MODELS:
            if model not in current:
                continue
                
            current_caps = current[model].get("capabilities", {})
            prev_caps = previous.get(model, {}).get("capabilities", {})
            
            if not prev_caps:
                changes.append(f"Added {model} to comparison.")
                continue
            
            # Compare each capability
            for category, caps in current_caps.items():
                if category not in prev_caps:
                    continue
                    
                for cap_name, cap_value in caps.items():
                    prev_value = prev_caps.get(category, {}).get(cap_name, "")
                    
                    if cap_value != prev_value:
                        changes.append(
                            f"{model}: {category} - {cap_name} changed from "
                            f"{prev_value} to {cap_value}"
                        )
        
        return changes if changes else ["No changes detected."]

    def validate_data(self, capabilities: Dict[str, Dict]) -> List[str]:
        """
        Validate capability data for consistency.
        
        Args:
            capabilities: Capability data to validate
            
        Returns:
            List of validation warnings/errors
        """
        warnings = []
        
        for model, data in capabilities.items():
            if "capabilities" not in data:
                warnings.append(f"{model}: Missing 'capabilities' key")
                continue
            
            caps = data["capabilities"]
            
            # Check all expected categories exist
            for category in CAPABILITIES.keys():
                if category not in caps:
                    warnings.append(f"{model}: Missing category '{category}'")
                    continue
                
                # Check all expected capabilities exist
                for cap in CAPABILITIES[category]:
                    if cap not in caps[category]:
                        warnings.append(
                            f"{model}: Missing capability '{cap}' in '{category}'"
                        )
                    else:
                        value = caps[category][cap]
                        if value not in [self.symbols["supported"], 
                                        self.symbols["not_supported"],
                                        self.symbols["partial"],
                                        self.symbols["best"]]:
                            warnings.append(
                                f"{model}: Invalid symbol '{value}' for '{cap}'"
                            )
        
        return warnings

