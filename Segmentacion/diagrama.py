from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def create_updated_process_diagram():

    fig, ax = plt.subplots(figsize=(14, 8))



    # Defining the updated process steps

    steps = [

        "Leer y Abrir Imagen", 

        "Preprocesamiento", 

        "Segmentación", 

        "Obtener Medidas y Bordes", 

        "Mostrar Resultados"

    ]

    substeps = [

        ["Leer ruta", "Abrir imagen"],

        ["Escala de grises", "Filtro mínimo", "Umbralizar", "Operación AND", "Guardar resultado"],

        ["Filtro gamma", "Top 2% brillante", "Descartar bordes", "Filtro mediana", "Máscara binaria", "Resaltar máscara"],

        ["Operador Prewitt", "Etiquetar objetos", "Calcular área", "Calcular perímetro", "Asignar valores"],

        []

    ]



    # Creating process boxes

    for i, step in enumerate(steps):

        rect = mpatches.FancyBboxPatch((0.05, 1 - 0.18 * i), 0.2, 0.15, boxstyle="round,pad=0.1", ec="none", color="skyblue")

        ax.add_patch(rect)

        ax.text(0.15, 1 - 0.18 * i + 0.075, step, ha="center", va="center", fontsize=12, color="black")

        

        substep_width = 0.12  # Adjusted width for substeps

        for j, substep in enumerate(substeps[i]):

            sub_rect = mpatches.FancyBboxPatch((0.3 + substep_width * j, 1 - 0.18 * i), substep_width, 0.15, boxstyle="round,pad=0.01", ec="none", color="lightgreen")

            ax.add_patch(sub_rect)

            ax.text(0.3 + substep_width * j + substep_width / 2, 1 - 0.18 * i + 0.075, substep, ha="center", va="center", fontsize=9, color="black", wrap=True)



    # Setting general plot properties

    ax.set_xlim(0, 1)

    ax.set_ylim(0, 1)

    ax.axis('off')



    return fig



# Create and display the updated process diagram with additional steps

fig = create_updated_process_diagram()

plt.show()
