import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

def create_category_chart(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    top_cat = df['Category'].value_counts().head(10)
    sns.barplot(x=top_cat.index, y=top_cat.values, palette='viridis', ax=ax)
    ax.set_title('Top 10 App Categories', fontsize=14)
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    return fig

def create_rating_density_chart(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.kdeplot(data=df, x='Rating', hue='Type', fill=True, palette='crest', ax=ax)
    ax.set_title('Rating Density: Free vs Paid', fontsize=14)
    plt.tight_layout()
    return fig

def create_price_vs_rating_chart(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    paid_apps = df[df['Type'] == 'Paid']
    sns.scatterplot(data=paid_apps, x='Price', y='Rating', alpha=0.6, ax=ax)
    ax.set_title('Price vs Rating (Paid Apps)', fontsize=14)
    plt.tight_layout()
    return fig