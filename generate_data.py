import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_dummy_data(n_rows=100):
    # Set seed for reproducibility
    np.random.seed(42)
    random.seed(42)

    base_date = datetime(2026, 3, 1)

    data = {
        'order_item_id': np.arange(10000000, 10000000 + n_rows),
        'order_id': np.random.randint(30000000, 32000000, size=n_rows),
        'order_item_type': np.random.choice(['Sale', 'Exchange', 'Return'], size=n_rows),
        'distribution_centre': ['JHB DC'] * n_rows,
        'sku_code': [f"{random.randint(1000, 9999)}-ABCD-{random.randint(1000, 9999)}" for _ in range(n_rows)],
        'product_description': np.random.choice(['Single-breasted blazer', 'Corduroy blazer', 'Linen-blend blazer', 'Mama wide jeans'], size=n_rows),
        
        # Columns with NULLS (for COALESCE testing)
        'promotional_code': [np.nan if random.random() > 0.1 else f"PROMO_{random.randint(10, 99)}" for _ in range(n_rows)],
        'cart_promotion_code': [np.nan if random.random() > 0.15 else f"CART_{random.randint(100, 999)}" for _ in range(n_rows)],
        
        'status': np.random.choice(['Shipped', 'Delivered', 'Processing'], size=n_rows),
        'shipped_date': [(base_date + timedelta(days=random.randint(1, 10))).strftime('%Y-%m-%d') for _ in range(n_rows)],
        'delivered_date': [np.nan if random.random() > 0.4 else (base_date + timedelta(days=random.randint(11, 20))).strftime('%Y-%m-%d') for _ in range(n_rows)],
        
        'unit_price_excl_vat': np.random.uniform(200, 700, size=n_rows).round(2),
    }

    df = pd.DataFrame(data)
    
    # Financial Calculation Example
    df['unit_price_incl_vat'] = (df['unit_price_excl_vat'] * 1.15).round(2)
    
    return df

# Create the dummy data
dummy_df = generate_dummy_data(100)

# --- COALESCE EXAMPLE IN PYTHON ---
# Create an 'Active Promo' column by taking the first non-null promo code
dummy_df['active_promo'] = dummy_df['promotional_code'].fillna(dummy_df['cart_promotion_code']).fillna('NONE')

# Save to CSV
dummy_df.to_csv('dummy_order_data.csv', index=False)
print("Dummy data generated and saved as 'dummy_order_data.csv'")
