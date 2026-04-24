import streamlit as st
import networkx as nx
import json
import os
import math
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

st.set_page_config(layout="wide", page_title="GreenMap - Campus Navigator")

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
NODES_FILE = os.path.join(ASSETS_DIR, "nodes.json")
MAP_FILE = os.path.join(ASSETS_DIR, "map.png")
PATHS_DIR = os.path.join(ASSETS_DIR, "paths")

WALKING_SPEED = 80
PIN_RADIUS = 15

academic_buildings = ["COS", "PCH", "JFH", "PBH", "PBH back", "Mariano Alvarez Hall", "ICTC"]
administrative_buildings = ["Ayunta", "Ayunta back", "Ayunta JFH", "Centennial Hall", "Alumni Building"]
university_facilities = ["Aklatan", "LCDC", "Botanical Garden", "Gourmet Hall", "Bridge", "Cultural Heritage Complex", "Camarin", "Museo", "Food Square"]
university_lodgings = ["JFH Kubo", "Residencia", "Hotel Rafael", "Male Dorm", "Female Dorm"]
parking = ["JFH Parking", "PBH Parking", "ICTC Parking", "Chapel Parking"]
chapel = ["Chapel"]
security_other = ["Gate 1"]


def load_nodes():
    with open(NODES_FILE, "r") as f:
        return json.load(f)


def build_graph():
    g = nx.Graph()

    academic_buildings = ["COS", "PCH", "JFH", "PBH", "PBH back", "Mariano Alvarez Hall", "ICTC"]
    administrative_buildings = ["Ayunta", "Ayunta back", "Ayunta JFH", "Centennial Hall", "Alumni Building"]
    university_facilities = ["Aklatan", "LCDC", "Botanical Garden", "Gourmet Hall", "Bridge", "Cultural Heritage Complex", "Camarin", "Museo", "Food Square"]
    university_lodgings = ["JFH Kubo", "Residencia", "Hotel Rafael", "Male Dorm", "Female Dorm"]
    parking = ["JFH Parking", "PBH Parking", "ICTC Parking", "Chapel Parking"]
    chapel = ["Chapel"]
    security_other = ["Gate 1"]

    nodes = academic_buildings + administrative_buildings + university_facilities + university_lodgings + parking + chapel + security_other
    g.add_nodes_from(nodes)

    edges_with_data = [
        ("COS", "Ayunta back", 10, "COS-Ayunta back"),
        ("Ayunta", "Ayunta back", 46, "Ayunta-Ayunta back"),
        ("Ayunta JFH", "Ayunta back", 70, "Ayunta JFH-Ayunta back"),
        ("Ayunta JFH", "Ayunta", 43, "Ayunta JFH-Ayunta"),
        ("Ayunta", "PCH", 30, "Ayunta-PCH"),
        ("Ayunta JFH", "JFH Parking", 85, "Ayunta-JFH Parking"),
        ("JFH Parking", "PCH", 59, "JFH Parking-PCH"),
        ("JFH Parking", "JFH", 30, "JFH Parking-JFH"),
        ("PCH", "JFH", 10, "PCH-JFH"),
        ("JFH", "JFH Kubo", 33, "JFH-JFH Kubo"),
        ("Gate 1", "JFH Kubo", 77, "Gate 1-JFH Kubo"),
        ("JFH Kubo", "PBH", 20, "JFH Kubo-PBH"),
        ("PBH back", "PBH", 60, "PBH back-PBH"),
        ("PBH", "Mariano Alvarez Hall", 88, "PBH-Mariano Alvarez Hall"),
        ("JFH Kubo", "Mariano Alvarez Hall", 75, "JFH Kubo-Mariano Alvarez Hall"),
        ("Mariano Alvarez Hall", "ICTC", 30, "Mariano Alvarez Hall-ICTC"),
        ("ICTC Parking", "ICTC", 39, "ICTC Parking - ICTC"),
        ("ICTC Parking", "Gate 1", 47, "ICTC Parking - Gate 1"),
        ("JFH Parking", "Gate 1", 36, "JFH Parking - Gate 1"),
        ("ICTC Parking", "Mariano Alvarez Hall", 29, "ICTC Parking - Mariano Alvarez Hall"),
        ("PBH back", "ICTC", 50, "PBH back-ICTC"),
        ("PBH Parking", "PBH back", 14, "PBH Parking-PBH back"),
        ("PBH Parking", "ICTC", 44, "PBH Parking-ICTC"),
        ("PBH Parking", "Gourmet Hall", 38, "PBH Parking-Gourmet Hall"),
        ("Centennial Hall", "Gourmet Hall", 43, "Centennial-Gourmet"),
        ("Centennial Hall", "Hotel Rafael", 27, "Centennial-Hotel Rafael"),
        ("Alumni Building", "Hotel Rafael", 82, "Alumni Building-Hotel Rafael"),
        ("Bridge", "Hotel Rafael", 53, "Bridge-Hotel Rafael"),
        ("Bridge", "Botanical Garden", 73, "Bridge-Botanical Garden"),
        ("Bridge", "Alumni Building", 106, "Bridge-Alumni Building"),
        ("Alumni Building", "Food Square", 215, "Alumni Building-Food Square"),
        ("Male Dorm", "Food Square", 38, "Male Dorm-Food Square"),
        ("Male Dorm", "Female Dorm", 133, "Male Dorm-Female Dorm"),
        ("COS", "Residencia", 142, "COS-Residencia"),
        ("Residencia", "Aklatan", 90, "Residencia-Aklatan"),
        ("JFH Kubo", "Aklatan", 205, "JFH Kubo-Aklatan"),
        ("JFH Kubo", "LCDC", 98, "JFH Kubo-LCDC"),
        ("Aklatan", "LCDC", 177, "Aklatan-LCDC"),
        ("Botanical Garden", "LCDC", 95, "Botanical Garden-LCDC"),
        ("Botanical Garden", "PBH", 100, "Botanical Garden-PBH"),
        ("Botanical Garden", "Aklatan", 95, "Botanical Garden-Aklatan"),
        ("Chapel", "Aklatan", 26, "Chapel - Aklatan"),
        ("Chapel", "Chapel Parking", 32, "Chapel - Chapel Parking"),
        ("Camarin", "Chapel Parking", 45, "Camarin - Chapel Parking"),
        ("Chapel", "Cultural Heritage Complex", 18, "Chapel - Cultural Heritage Complex"),
        ("Aklatan", "Cultural Heritage Complex", 52, "Aklatan - Cultural Heritage Complex"),
        ("Camarin", "Cultural Heritage Complex", 60, "Camarin - Cultural Heritage Complex"),
        ("Museo", "Cultural Heritage Complex", 100, "Museo - Cultural Heritage Complex"),
        ("Botanical Garden", "Cultural Heritage Complex", 100, "Botanical Garden - Cultural Heritage Complex"),
        ("Museo", "Botanical Garden", 98, "Museo - Botanical Garden"),
        ("Museo", "Food Square", 98, "Museo - Food Square")
    ]

    for u, v, weight, name in edges_with_data:
        g.add_edge(u, v, weight=weight, name=name)

    return g


def calculate_walking_time(distance_m):
    minutes = distance_m / WALKING_SPEED
    if minutes < 1:
        return "Less than a minute walk"
    return f"{int(math.ceil(minutes))} minute walk"


def get_pin_color(node, start_node, target_node, route=None):
    if route and node in route:
        if node == start_node:
            return "#00FF00"
        elif node == target_node:
            return "#FF0000"
        elif node in route:
            return "#90EE90"
        return "#FFFFFF"
    elif node == start_node:
        return "#00FF00"
    elif node == target_node:
        return "#FF0000"
    return "#FFFFFF"


def get_pin_size(node, start_node, target_node):
    if node == start_node or node == target_node:
        return 22
    return 15


def render_map(nodes, start_node, target_node, route=None):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    ax.set_xlim(0, 1920)
    ax.set_ylim(1080, 0)
    ax.set_aspect('equal')
    ax.axis('off')

    if os.path.exists(MAP_FILE):
        map_img = Image.open(MAP_FILE)
        map_img = map_img.transpose(Image.FLIP_TOP_BOTTOM)
        ax.imshow(map_img, extent=[0, 1920, 0, 1080])
    else:
        ax.set_facecolor('#2A2A2A')
        ax.text(960, 540, 'map.png not found\nAdd your map image to assets/', 
                ha='center', va='center', color='white', fontsize=16)

def render_map(nodes, start_node, target_node, route=None):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=120)
    ax.set_xlim(0, 1920)
    ax.set_ylim(1080, 0)
    ax.set_aspect('equal')
    ax.axis('off')

    if os.path.exists(MAP_FILE):
        map_img = Image.open(MAP_FILE)
        map_img = map_img.transpose(Image.FLIP_TOP_BOTTOM)
        ax.imshow(map_img, extent=[0, 1920, 0, 1080])
    else:
        ax.set_facecolor('#2A2A2A')
        ax.text(960, 540, 'map.png not found\nAdd your map image to assets/', 
                ha='center', va='center', color='white', fontsize=16)

    if route:
        path_edges = list(zip(route, route[1:]))
        for i, edge in enumerate(path_edges):
            node_a, node_b = edge
            path_file = os.path.join(PATHS_DIR, f"{node_a}-{node_b}.png")
            if not os.path.exists(path_file):
                path_file = os.path.join(PATHS_DIR, f"{node_b}-{node_a}.png")
            
            if os.path.exists(path_file):
                path_img = Image.open(path_file).convert('RGBA')
                path_img = path_img.transpose(Image.FLIP_TOP_BOTTOM)
                ax.imshow(path_img, extent=[0, 1920, 0, 1080], alpha=0.9)

    for node_name, node_data in nodes.items():
        x = node_data.get("x")
        y = node_data.get("y")
        if x is None or y is None:
            continue

        color = get_pin_color(node_name, start_node, target_node, route)
        radius = get_pin_size(node_name, start_node, target_node)
        
        circle = plt.Circle((x, y), radius, color=color, ec='black', 
                           linewidth=2, zorder=10, alpha=0.9)
        ax.add_patch(circle)

        ax.annotate(node_data.get("label", node_name), (x, y - 25), 
                   ha='center', va='top', fontsize=8, color='white',
                   fontweight='bold', zorder=11)

    return fig


def main():
    st.title("GreenMap - Campus Navigator")

    if "start_node" not in st.session_state:
        st.session_state.start_node = None
    if "target_node" not in st.session_state:
        st.session_state.target_node = None

    nodes = load_nodes()
    graph = build_graph()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Current Location")
        current_display = st.session_state.start_node if st.session_state.start_node else "---"
        st.markdown(f"**:green●** {current_display}")

    with col2:
        st.markdown("### Target Destination")
        target_display = st.session_state.target_node if st.session_state.target_node else "---"
        st.markdown(f"**:red●** {target_display}")

    st.markdown("---")

    nodes_list = sorted(nodes.keys())

    col_sel1, col_sel2 = st.columns(2)
    with col_sel1:
        selected_start = st.selectbox(
            "Select Start Location",
            options=[""] + nodes_list,
            index=0 if not st.session_state.start_node else nodes_list.index(st.session_state.start_node) + 1,
            key="start_select"
        )
        if selected_start:
            st.session_state.start_node = selected_start

    with col_sel2:
        options_for_target = [n for n in nodes_list if n != st.session_state.start_node]
        selected_target = st.selectbox(
            "Select Target Location",
            options=[""] + options_for_target,
            index=0 if not st.session_state.target_node else options_for_target.index(st.session_state.target_node) + 1,
            key="target_select"
        )
        if selected_target:
            st.session_state.target_node = selected_target

    if st.button("Reset"):
        st.session_state.start_node = None
        st.session_state.target_node = None
        st.rerun()

    st.markdown("---")

    start = st.session_state.start_node
    target = st.session_state.target_node

    if start and target:
        try:
            shortest_path = nx.shortest_path(graph, source=start, target=target, weight="weight")
            total_distance = nx.shortest_path_length(graph, source=start, target=target, weight="weight")
            walking_time = calculate_walking_time(total_distance)

            fig = render_map(nodes, start, target, route=shortest_path)
            st.pyplot(fig)

            st.markdown("---")
            st.markdown("### Route Details")

            route_display = " → ".join(shortest_path)
            st.markdown(f"**Route:** {route_display}")
            st.markdown(f"**Distance:** {total_distance} m")
            st.markdown(f"**Walking Time:** {walking_time}")

            with st.expander("See Node-by-Node Breakdown"):
                for i, node in enumerate(shortest_path):
                    st.markdown(f"{i+1}. {node}")

        except nx.NetworkXError:
            st.error(f"No path found between {start} and {target}")
    else:
        fig = render_map(nodes, start, target)
        st.pyplot(fig)
        st.info("Select both start and target locations to see the route.")

    st.markdown("---")
    with st.expander("Setup Instructions"):
        st.markdown("""
        **To complete setup:**

        1. Add your `map.png` (1920x1080) to `assets/map.png`
        2. Edit `assets/nodes.json` and add X,Y coordinates for each node
        3. Create transparent path PNGs in `assets/paths/` folder:
           - Naming: `{nodeA}-{nodeB}.png` (e.g., `COS-Ayunta back.png`)
           - Same dimensions as map.png (1920x1080)
           - Blue path color for visibility
        """)


if __name__ == "__main__":
    main()