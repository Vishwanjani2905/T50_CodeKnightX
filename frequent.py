import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your CSV file
file_path = r"C:\Users\vishw\Downloads\problem 1 (Csv file )\problem 1\Cleaned_Smart_Warehousing_Dataset.csv"
df = pd.read_csv(file_path)

# Check if 'Category Name' exists in the DataFrame
if 'Category Name' in df.columns:
    print("Category Name column found.")
    category_frequency = df['Category Name'].value_counts()
    sorted_categories = category_frequency.sort_values(ascending=False)

    print("\nCategories sorted by frequency of occurrence:")
    print(sorted_categories)

    # Plotting the bar chart using seaborn
    plt.figure(figsize=(14, 10))
    sns.set(style="whitegrid")
    
    # Use top 30 categories for better visibility
    top_n = 30
    sns.barplot(
        x=sorted_categories.values[:top_n], 
        y=sorted_categories.index[:top_n],
        palette='viridis'  # You can try 'coolwarm', 'cubehelix', 'magma', etc.
    )

    plt.title("Top 30 Most Frequent Product Categories", fontsize=16)
    plt.xlabel("Frequency", fontsize=12)
    plt.ylabel("Category Name", fontsize=12)
    plt.tight_layout()
    plt.show()

else:
    print("Warning: 'Category Name' column not found.")
