import pandas as pd
import numpy as np

def clean_currency(price_str):
    """
    Removes '$' and converts to float. Returns NaN if conversion fails.
    """
    if isinstance(price_str, str):
        clean_str = price_str.replace('$', '').strip()
        try:
            return float(clean_str)
        except ValueError:
            return np.nan
    return price_str

def clean_installs(install_str):
    """
    Removes '+' and ',' and converts to float. Returns NaN if conversion fails.
    """
    if isinstance(install_str, str):
        # Remove unwanted characters
        cleaned = install_str.replace('+', '').replace(',', '').strip()
        
        # Handle specific edge cases found in this dataset
        if cleaned == 'Free': 
            return 0.0
        if cleaned == 'Everyone': # <--- This fixes your specific error
            return np.nan
            
        try:
            return float(cleaned)
        except ValueError:
            return np.nan
    return install_str

def clean_size(size_str):
    """
    Converts 'M' (Millions) and 'k' (Thousands) to bytes.
    """
    if isinstance(size_str, str):
        size_str = size_str.strip()
        try:
            if 'M' in size_str:
                return float(size_str.replace('M', '')) * 1_000_000
            elif 'k' in size_str:
                return float(size_str.replace('k', '')) * 1_000
            elif size_str == 'Varies with device':
                return np.nan
            else:
                # Try direct conversion just in case
                return float(size_str)
        except ValueError:
            return np.nan
    return float(size_str)

def load_and_process_data(uploaded_file):
    """
    Reads the uploaded CSV file and cleans it robustly.
    """
    # Read CSV from the uploaded file object
    df = pd.read_csv(uploaded_file)

    # Drop duplicates
    df.drop_duplicates(inplace=True)
    
    # Cleaning columns with safe functions
    df['Installs'] = df['Installs'].apply(clean_installs)
    df['Price'] = df['Price'].apply(clean_currency)
    df['Size_Bytes'] = df['Size'].apply(clean_size)
    
    # Clean Reviews (Coerce errors to NaN automatically)
    df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
    
    # Clean Rating (Coerce errors to NaN automatically)
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # Drop rows where critical data is missing (NaN)
    # This will now automatically drop the 'Everyone' row
    df.dropna(subset=['Rating', 'Installs', 'Price'], inplace=True)

    return df