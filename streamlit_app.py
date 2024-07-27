import rdflib
import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

# URL до Unified Cyber Ontology у форматі RDF/XML
UCO_URL = "https://ontology.unifiedcyberontology.org/owl"

# Завантаження онтології
g = rdflib.Graph()
try:
    g.parse(UCO_URL, format='xml')
except Exception as e:
    st.error(f"Failed to load ontology: {e}")

# Функція для очищення та форматування URI
def format_uri(uri):
    # Видаляє частину URI до останнього сегмента
    return uri.rsplit('/', 1)[-1]

# Функція для створення вузлів і ребер для графу
def create_graph_data(graph):
    nodes = {}
    edges = set()

    for subj, pred, obj in graph:
        subj_str = format_uri(str(subj))
        obj_str = format_uri(str(obj))
        pred_str = str(pred)

        # Додаємо вузли
        if subj_str not in nodes:
            nodes[subj_str] = Node(id=subj_str, label=subj_str)
        if obj_str not in nodes:
            nodes[obj_str] = Node(id=obj_str, label=obj_str)

        # Додаємо ребра
        edge_id = (subj_str, obj_str, pred_str)
        if edge_id not in edges:
            edges.add(edge_id)
    
    # Перетворюємо set в список
    edges = [Edge(source=edge[0], target=edge[1], label=edge[2]) for edge in edges]

    return list(nodes.values()), edges

# Створення вузлів і ребер
nodes, edges = create_graph_data(g)

# Конфігурація для agraph
config = Config(
    width=800,
    height=800,
    directed=True,
    nodeHighlightBehavior=True,
    highlightColor="#F7A7A6",
    collapsible=True,
    node={'labelProperty': 'label'},
    link={'labelProperty': 'label', 'renderLabel': True}
)

# Відображення графу
st.title("Unified Cyber Ontology Visualization")
agraph(nodes=nodes, edges=edges, config=config)

