# Separate functions - EASY TO READ! ✅
import pandas as pd

def load_data(filepath):
    """Load data from CSV file"""
    return pd.read_csv(filepath)

def clean_data(df):
    """Clean data by removing missing values and adding columns"""
    df = df.dropna()
    df['new_col'] = df['col1'] + df['col2']
    return df

def aggregate_data(df):
    """Aggregate data by category"""
    return df.groupby('category').mean()

# Main workflow
df = load_data('data.csv')
df_clean = clean_data(df)
result = aggregate_data(df_clean)

#################3##########################################################
# 1. PACKAGES: Import existing code
import pandas as pd

# 2. CLASSES: Create objects with data and methods
class DataProcessor:
    def __init__(self, data):
        self.data = data
    
    def clean(self):
        self.data = self.data.dropna()
        return self.data
    
    def aggregate(self, column):
        return self.data.groupby(column).mean()

# 3. METHODS: Functions that belong to classes/objects
df = pd.DataFrame(data)
df.plot('x', 'y')  # plot is a method of DataFrame

###############################################################################
# test_example.py

def test_clean_data():
    """Test that clean_data removes missing values"""
    df = pd.DataFrame({
        'category': ['A', 'B', None],
        'sales': [100, 200, 300]
    })
    
    df_clean = clean_data(df)
    
    assert len(df_clean) == 2
    assert df_clean['category'].isna().sum() == 0

def test_calculate_sales_summary():
    """Test sales summary calculation"""
    df = pd.DataFrame({
        'category': ['A', 'A', 'B', 'B'],
        'sales': [100, 200, 300, 400]
    })
    
    summary = calculate_sales_summary(df)
    
    assert summary['A'] == 150
    assert summary['B'] == 350

# Run all tests
if __name__ == "__main__":
    test_clean_data()
    test_calculate_sales_summary()
    print("All tests passed! ✅")