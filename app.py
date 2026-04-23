import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
g = nx.Graph()

academic_buildings=["COS","PCH","JFH","PBH","PBH back","Mariano Alvarez Hall","ICTC"]
administrative_buildings=["Ayunta","Ayunta back","Ayunta JFH","Centennial Hall","Alumni Building"]
university_facilities=["Aklatan", "LCDC", "Botanical Garden", "Gourmet Hall", "Bridge", "Cultural Heritage Complex", "Camarin", "Museo", "Food Square"]
university_lodgings=["JFH Kubo", "Residencia", "Hotel Rafael", "Male Dorm", "Female Dorm"]
parking=["JFH Parking", "PBH Parking", "ICTC Parking", "Chapel Parking"]
chapel=["Chapel"]
security_other=["Gate 1"]

nodes= academic_buildings + administrative_buildings + university_facilities + university_lodgings + parking + chapel + security_other
g.add_nodes_from(nodes)
edges_with_data = [
    ("COS", "Ayunta back", 10, "COS-Ayunta back"),
    ("Ayunta", "Ayunta back", 46, "Ayunta-Ayunta back"),
    ("Ayunta JFH", "Ayunta back", 70, "Ayunta JFH-Ayunta back"),
    ("Ayunta JFH", "Ayunta", 43, "Ayunta JFH-Ayunta"),
    ("Ayunta", "PCH", 30, "Ayunta-PCH"),
    ("Ayunta JFH", "JFH Parking", 85, "Ayunta-JFH Parking"),
    ("JFH Parking", "PCH", 59, "JFH Parking-PCH"),
    ("JFH Parking", "JFH", 14, "JFH Parking-JFH"),
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

pos = nx.spring_layout(g,weight=weight,k=0.15,iterations=50,seed=5)

start_node = "Gate 1"
end_node = "Food Square"

shortest_path = nx.shortest_path(g, source=start_node, target=end_node, weight="weight")
total_distance = nx.shortest_path_length(g, source=start_node, target=end_node, weight="weight")

path_edges = list(zip(shortest_path, shortest_path[1:]))

print(f"--- Trip Info ---")
print(f"Start: {start_node}")
print(f"End:   {end_node}")
print(f"Route: {' -> '.join(shortest_path)}")
print(f"Total Distance: {total_distance} m")

colors = {
    "Academic": "#4169E1",
    "Admin": "#00C957",
    "Facilities": "#FFD700",
    "Lodgings": "#FF69B4",
    "Parking": "#696969",
    "Chapel": "#808080",
    "Security": "#505050"
}

node_color_map = {}
for node in g.nodes():
    if node in academic_buildings:
        node_color_map[node] = colors["Academic"]
    elif node in administrative_buildings:
        node_color_map[node] = colors["Admin"]
    elif node in university_facilities:
        node_color_map[node] = colors["Facilities"]
    elif node in university_lodgings:
        node_color_map[node] = colors["Lodgings"]
    elif node in parking:
        node_color_map[node] = colors["Parking"]
    elif node in chapel:
        node_color_map[node] = colors["Chapel"]
    elif node in security_other:
        node_color_map[node] = colors["Security"]
    else:
        node_color_map[node] = "#D3D3D3"

plt.figure(figsize=(15, 12))

node_colors_list = [node_color_map[n] for n in g.nodes()]
edge_colors_list = ['red' if n == start_node or n == end_node else '#333333' for n in g.nodes()]
line_widths_list = [3.0 if n == start_node or n == end_node else 1.5 for n in g.nodes()]

nx.draw_networkx_nodes(g, pos,node_color=node_colors_list,node_size=2500,edgecolors=edge_colors_list,linewidths=line_widths_list)
nx.draw_networkx_edges(g, pos, edge_color='#AAAAAA', width=1.0)
nx.draw_networkx_edges(g, pos, edgelist=path_edges, edge_color='#FF4500',width=3.5)
nx.draw_networkx_labels(g, pos, font_size=10, font_weight='bold', font_color='#000080')

legend_patches = [
    mpatches.Patch(color=colors["Academic"], label='Academic Building'),
    mpatches.Patch(color=colors["Admin"], label='Administrative Building'),
    mpatches.Patch(color=colors["Facilities"], label='University Facilities'),
    mpatches.Patch(color=colors["Lodgings"], label='Lodgings & Learning'),
    mpatches.Patch(color=colors["Parking"], label='Parking'),
    mpatches.Patch(color=colors["Chapel"], label='Chapel'),
    mpatches.Patch(color=colors["Security"], label='Security/Gates'),
]
plt.legend(handles=legend_patches, loc='center right', bbox_to_anchor=(1, 1), title="Legend")
plt.title(f"Campus Map - Shortest Path ({total_distance} m) from {start_node} to {end_node}", fontsize=16)
plt.axis('off')
plt.show()
