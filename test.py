import json
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter


# Load JSON data
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


# Convert JSON to DataFrames
def json_to_dataframes(data):
    nodes_df = pd.DataFrame(data['nodes'])
    edges_df = pd.DataFrame(data['edges'])
    return nodes_df, edges_df


# Plot bar chart for categorical columns
def plot_bar(df, column, title, top_n=None, figsize=(10, 6)):
    counts = df[column].value_counts()
    if top_n:
        counts = counts.head(top_n)
    plt.figure(figsize=figsize)
    sns.barplot(x=counts.values, y=counts.index, palette="viridis")
    plt.title(f"{title} (Top {top_n})" if top_n else title)
    plt.xlabel("Count")
    plt.ylabel(column)
    plt.show()


# Plot degree distribution
def plot_degree_distribution(G):
    degrees = [d for n, d in G.degree()]
    plt.figure(figsize=(10, 6))
    sns.histplot(degrees, bins=30, kde=False, color="skyblue")
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Count")
    plt.show()


# Plot top entities by degree
def plot_top_entities(G, top_n=20):
    degrees = dict(G.degree())
    top_entities = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_df = pd.DataFrame(top_entities, columns=["Entity", "Degree"])
    plt.figure(figsize=(12, 8))
    sns.barplot(x="Degree", y="Entity", data=top_df, palette="magma")
    plt.title(f"Top {top_n} Entities by Degree (Connections)")
    plt.show()


# Analyze edge types and inferred edges
def analyze_edges(edges_df):
    # Edge type distribution
    plot_bar(edges_df, "type", "Edge Type Distribution")

    # Inferred edges (True/False)
    if "is_inferred" in edges_df.columns:
        inferred_counts = edges_df["is_inferred"].value_counts()
        plt.figure(figsize=(6, 4))
        sns.barplot(x=inferred_counts.index, y=inferred_counts.values, palette="pastel")
        plt.title("Inferred Edges (True/False)")
        plt.show()


# Temporal analysis (if date columns exist)
def analyze_temporal(nodes_df):
    if "date" in nodes_df.columns:
        nodes_df["date"] = pd.to_datetime(nodes_df["date"], errors="coerce")
        temporal_counts = nodes_df["date"].dt.to_period("M").value_counts().sort_index()
        plt.figure(figsize=(12, 6))
        temporal_counts.plot(kind="line", marker="o")
        plt.title("Activity Over Time (Monthly)")
        plt.xlabel("Date")
        plt.ylabel("Count")
        plt.grid()
        plt.show()


# Main execution
if __name__ == '__main__':
    file_path = r"C:\Users\Tianlung\PycharmProjects\pythonProject1\MC3_release\MC3_graph.json"  # Replace with your file
    data = load_json(file_path)
    nodes_df, edges_df = json_to_dataframes(data)

    # --- Visualizations ---
    # 1. Node subtypes (e.g., sub_type, type)
    plot_bar(nodes_df, "sub_type", "Node Sub-Types", top_n=20)
    plot_bar(nodes_df, "type", "Node Types", top_n=20)

    # 2. Load into NetworkX for degree analysis
    G = nx.Graph()
    G.add_nodes_from(nodes_df["id"].tolist())
    G.add_edges_from([(e["source"], e["target"]) for _, e in edges_df.iterrows()])

    # Degree distribution (1 vs. 3+ connections)
    plot_degree_distribution(G)

    # 3. Top entities by degree (ranking)
    plot_top_entities(G, top_n=20)

    # 4. Edge analysis
    analyze_edges(edges_df)

    # 5. Temporal trends (if date exists)
    analyze_temporal(nodes_df)

    # --- Additional Stats ---
    print("\nAdditional Statistics:")
    print(f"Average degree: {sum(dict(G.degree()).values()) / len(G):.2f}")
    print(f"Nodes with degree 1: {sum(1 for _, d in G.degree() if d == 1)}")
    print(f"Nodes with degree >=3: {sum(1 for _, d in G.degree() if d >= 3)}")
    print(f"Connected components: {nx.number_connected_components(G)}")