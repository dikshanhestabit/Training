import pandas as pd
import numpy as np
import os
import json
import logging
from scipy.stats import ks_2samp, chi2_contingency

# Configuring logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_drift(reference_path, current_path, output_path='monitoring/drift_report.json'):
    try:
        logger.info("Starting production drift check (Raw-to-Raw)...")
        
        if not os.path.exists(reference_path):
            logger.error(f"Reference data not found at {reference_path}")
            return
        
        if not os.path.exists(current_path):
            logger.warning(f"No production logs found at {current_path}.")
            return

        ref_df = pd.read_csv(reference_path)
        cur_df = pd.read_csv(current_path)
        
        # Features to monitor (from the logs)
        features = [
            'age', 'workclass', 'education.num', 'marital.status', 
            'occupation', 'relationship', 'race', 'sex', 
            'capital.gain', 'capital.loss', 'hours.per.week', 'native.country'
        ]
        
        drift_results = {}
        global_drift = False
        
        for col in features:
            if col not in ref_df.columns or col not in cur_df.columns:
                continue
                
            # 1. Numerical Drift (KS Test)
            if pd.api.types.is_numeric_dtype(ref_df[col]):
                stat, p_value = ks_2samp(ref_df[col], cur_df[col])
                method = "Kolmogorov-Smirnov"
            
            # 2. Categorical Drift (Chi-Square)
            else:
                # Combining categories to ensure alignment
                ref_counts = ref_df[col].value_counts()
                cur_counts = cur_df[col].value_counts()
                
                # Align counts
                all_cats = list(set(ref_counts.index) | set(cur_counts.index))
                ref_aligned = [ref_counts.get(cat, 0) for cat in all_cats]
                cur_aligned = [cur_counts.get(cat, 0) for cat in all_cats]
                
                # Chi2 needs at least some data in each group
                if sum(cur_aligned) > 0:
                    try:
                        stat, p_value, _, _ = chi2_contingency([ref_aligned, cur_aligned])
                        method = "Chi-Square"
                    except:
                        p_value = 1.0 # Fallback
                        method = "Chi-Square (Failed)"
                else:
                    p_value = 1.0
                    method = "Not enough data"

            is_drift = p_value < 0.05
            if is_drift:
                global_drift = True
            
            drift_results[col] = {
                'p_value': float(p_value),
                'drift_detected': bool(is_drift),
                'method': method
            }
            logger.info(f"Feature '{col}': p-value={p_value:.4f}, Drift={is_drift} ({method})")
            
        report = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'global_drift': global_drift,
            'reference_source': reference_path,
            'details': drift_results
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=4)
            
        logger.info(f"Drift report saved to {output_path}")
        return report

    except Exception as e:
        logger.error(f"Error during drift check: {e}")

if __name__ == "__main__":
    # RAW training data (to match raw user logs)
    REF_DATA = os.path.join('data', 'raw', 'adult.csv')
    PROD_LOGS = os.path.join('monitoring', 'prediction_logs.csv')
    
    check_drift(REF_DATA, PROD_LOGS)
