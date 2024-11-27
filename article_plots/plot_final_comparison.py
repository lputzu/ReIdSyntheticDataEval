# import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Creazione dei dati estratti dalla tabella

Market_index = [0,1,2,3]
Duke_index = [4,5,6,7]
MSMT_index = [8,9,10,11]

map_index = [0, 4, 8]
R1_index = [1, 5, 9]
R5_index = [2, 6, 10]
R10_index = [3, 7, 11]

Downloaded_Resnet_50 = {
"FineGPR" : [9.9 , 27.6 , 45.0 , 52.0 , 11.0 , 26.8 , 39.2 , 45.3 , 4.4 , 19.0 , 29.6 , 34.9],
"UnrealPerson":  [41.7 , 70.8 , 82.8 , 87.4 , 41.6 , 64.6 , 76.5 , 81.0 , 11.3 , 30.9 , 42.8 , 48.8],
"ClonedPerson": [47.6 , 77.1 , 89.9 , 93.3 , 33.8 , 57.8 , 71.9 , 76.9 , 8.6 , 26.4 , 39.4 , 45.3],
"WePerson": [9.4 , 24.1 , 41.3 , 50.1 , 10.8 , 27.6 , 38.8 , 44.7 , 2.7 , 11.7 , 20.9 , 25.4],
"PersonX": [21.8 , 45.4 , 63.3 , 70.3 , 17.2 , 33.5 , 46.2 , 52.2 , 2.7 , 8.8 , 15.2 , 19.1],
"RandPerson": [29.9 , 58.7 , 75.2 , 81.1 , 25.2 , 46.1 , 61.3 , 67.1 , 4.7 , 15.6 , 24.7 , 29.5]}

Downloaded_ViT_Small = {
"FineGPR": [9.9 , 27.6 , 45.0 , 52.0 , 11.0 , 26.8 , 39.2 , 45.3 , 4.4 , 19.0 , 29.6 , 34.9],
"UnrealPerson": [23.1 , 46.2 , 63.4 , 70.2 , 25.3 , 44.0 , 60.9 , 66.9 , 4.2 , 12.8 , 22.9 , 28.6],
"ClonedPerson": [47.6 , 77.1 , 89.9 , 93.3 , 33.8 , 57.8 , 71.9 , 76.9 , 8.6 , 26.4 , 39.4 , 45.3],
"WePerson": [9.4 , 24.1 , 41.3 , 50.1 , 10.8 , 27.6 , 38.8 , 44.7 , 2.7 , 11.7 , 20.9 , 25.4],
"PersonX": [21.8 , 45.4 , 63.3 , 70.3 , 17.2 , 33.5 , 46.2 , 52.2 , 2.7 , 8.8 , 15.2 , 19.1],
"RandPerson": [29.9 , 58.7 , 75.2 , 81.1 , 25.2 , 46.1 , 61.3 , 67.1 , 4.7 , 15.6 , 24.7 , 29.5]}

Subset_Resnet_50 = {
"FineGPR" : [9.9, 31.4 , 46.5 , 52.9  , 9.5 , 26.3 , 36.5 , 41.7 , 3.8 , 19.2 , 28.8 , 33.3],
"UnrealPerson": [40.2 , 71.4 , 83.8 , 87.4 , 40.3 , 65.8 , 76.9 , 81.0 , 12.6 , 35.7 , 47.8 , 52.8],
"ClonedPerson": [37.4 , 70.5 , 83.9 , 88.6 , 29.3 , 53.7 , 69.0 , 74.3 , 7.2 , 24.6 , 35.7 , 40.9],
"WePerson": [25.9 , 53.6 , 59.1 , 74.7 , 21.7 , 40.9 , 54.8 , 60.3 , 4.4 , 14.7 , 23.4 , 27.9]}

Subset_ViT_Small = {
"FineGPR" : [22.4 , 47.0 , 63.7 , 70.6 , 26.1 , 44.7 , 60.5 , 65.7 , 7.4 , 22.4 , 34.2 , 39.7],
"UnrealPerson":  [32.0 , 58.9 , 74.2 , 79.7 , 34.0 , 53.3 , 68.3 , 73.4 , 10.0 , 27.4 , 39.3 , 45.2],
"ClonedPerson": [27.9 , 53.5 , 69.3 , 76.0 , 25.8 , 44.0 , 59.1 , 65.6 , 5.5 , 16.4 , 26.4 , 32.0],
"WePerson": [20.2 , 42.3 , 58.1 , 65.1 , 25.1 , 39.9 , 56.0 , 62.1 , 5.6 , 15.7 , 25.4 , 30.4]}


models = {
    "Resnet_50": {
        "FineGPR (D)": [9.9, 27.6, 45.0, 52.0, 11.0, 26.8, 39.2, 45.3, 4.4, 19.0, 29.6, 34.9],
        "FineGPR (S)" : [9.9, 31.4 , 46.5 , 52.9  , 9.5 , 26.3 , 36.5 , 41.7 , 3.8 , 19.2 , 28.8 , 33.3],
        "UnrealPerson (D)": [41.7, 70.8, 82.8, 87.4, 41.6, 64.6, 76.5, 81.0, 11.3, 30.9, 42.8, 48.8],
        "UnrealPerson (S)": [40.2 , 71.4 , 83.8 , 87.4 , 40.3 , 65.8 , 76.9 , 81.0 , 12.6 , 35.7 , 47.8 , 52.8],
        "ClonedPerson (D)": [47.6, 77.1, 89.9, 93.3, 33.8, 57.8, 71.9, 76.9, 8.6, 26.4, 39.4, 45.3],
        "ClonedPerson (S)": [37.4 , 70.5 , 83.9 , 88.6 , 29.3 , 53.7 , 69.0 , 74.3 , 7.2 , 24.6 , 35.7 , 40.9],
        "WePerson (D)": [9.4, 24.1, 41.3, 50.1, 10.8, 27.6, 38.8, 44.7, 2.7, 11.7, 20.9, 25.4],
        # "": [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0], # non esiste
        "PersonX (D)": [21.8, 45.4, 63.3, 70.3, 17.2, 33.5, 46.2, 52.2, 2.7, 8.8, 15.2, 19.1],
        "PersonX (S)": [21.8, 45.4, 63.3, 70.3, 17.2, 33.5, 46.2, 52.2, 2.7, 8.8, 15.2, 19.1],
        "RandPerson (D)": [29.9, 58.7, 75.2, 81.1, 25.2, 46.1, 61.3, 67.1, 4.7, 15.6, 24.7, 29.5],
        # " ": [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]# non esiste
    },
    "ViT_Small": {
        "FineGPR (D)": [9.9, 27.6, 45.0, 52.0, 11.0, 26.8, 39.2, 45.3, 4.4, 19.0, 29.6, 34.9], # da modificare
        "FineGPR (S)" : [22.4 , 47.0 , 63.7 , 70.6 , 26.1 , 44.7 , 60.5 , 65.7 , 7.4 , 22.4 , 34.2 , 39.7],
        "UnrealPerson (D)": [23.1, 46.2, 63.4, 70.2, 25.3, 44.0, 60.9, 66.9, 4.2, 12.8, 22.9, 28.6],
        "UnrealPerson (S)":  [32.0 , 58.9 , 74.2 , 79.7 , 34.0 , 53.3 , 68.3 , 73.4 , 10.0 , 27.4 , 39.3 , 45.2],
        "ClonedPerson (D)": [47.6, 77.1, 89.9, 93.3, 33.8, 57.8, 71.9, 76.9, 8.6, 26.4, 39.4, 45.3],
        "ClonedPerson (S)": [27.9 , 53.5 , 69.3 , 76.0 , 25.8 , 44.0 , 59.1 , 65.6 , 5.5 , 16.4 , 26.4 , 32.0],
        "WePerson (D)": [9.4, 24.1, 41.3, 50.1, 10.8, 27.6, 38.8, 44.7, 2.7, 11.7, 20.9, 25.4],
        # "": [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0], # non esiste
        "PersonX (D)": [21.8, 45.4, 63.3, 70.3, 17.2, 33.5, 46.2, 52.2, 2.7, 8.8, 15.2, 19.1],
        "PersonX (S)": [21.8, 45.4, 63.3, 70.3, 17.2, 33.5, 46.2, 52.2, 2.7, 8.8, 15.2, 19.1],
        "RandPerson (D)": [29.9, 58.7, 75.2, 81.1, 25.2, 46.1, 61.3, 67.1, 4.7, 15.6, 24.7, 29.5],
        # " ": [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0] # non esiste
    }
}


# Estrarre i dati mAP
targets = ["Market", "Duke", "MSMT"]
colors = {"Market": "blue", "Duke": "orange", "MSMT": "green"}
patterns = ["", "//", "\\\\", "..", "**", "xx"]

# Preparazione dei dati per il plot
data = []
labels = list(models["Resnet_50"].keys())  # Dataset source
models_keys = list(models.keys())

x_positions = []
x_ticks_labels = []
bar_width = 0.2
n_targets = len(targets)
group_width = bar_width * n_targets * len(models_keys)
start_pos = 0

# Organizzazione dei dati
for label_idx, label in enumerate(labels):
    for model_idx, model in enumerate(models_keys):
        dataset = models[model][label]
        for target_idx, target in enumerate(targets):
            x_pos = start_pos + model_idx * n_targets * bar_width + target_idx * bar_width
            x_positions.append(x_pos)
            data.append((label, model, target, dataset[map_index[target_idx]]))
    x_ticks_labels.append(label)
    start_pos += group_width + 0.3  # Spazio tra i gruppi

# Plot
fig, ax = plt.subplots(figsize=(14, 6))
for idx, (source, model, target, value) in enumerate(data):
    pattern = patterns[models_keys.index(model)]
    color = colors[target]
    ax.bar(
        x_positions[idx],
        value,
        bar_width,
        color=color,
        edgecolor="black",
        hatch=pattern,
        label=f"{model}-{target}" if idx < len(models_keys) * n_targets else None
    )

# Creazione della legenda
handles, labels = ax.get_legend_handles_labels()
unique_labels = {label: handle for label, handle in zip(labels, handles)}
ax.legend(unique_labels.values(), unique_labels.keys(), title="Legend", bbox_to_anchor=(1.05, 1), loc='upper left')

# Personalizzazione dell'asse X
ax.set_xticks(
    [i * (group_width + 0.3) + group_width / 2 - bar_width * n_targets for i in range(len(x_ticks_labels))]
)
ax.set_xticklabels(x_ticks_labels, rotation=45)
ax.set_ylabel("mAP")
ax.set_title("mAP per Dataset Source, Modello e Target")

plt.tight_layout()
plt.show()



target_indices = {"Market": Market_index, "Duke": Duke_index, "MSMT": MSMT_index}

# Indici delle metriche
R1_index = 1
R5_index = 2
R10_index = 3
metrics = {"R1": R1_index, "R5": R5_index, "R10": R10_index}


# Colori per le metriche e target
base_colors = {"Market": "blue", "Duke": "orange", "MSMT": "green"}
metric_shades = {"R1": 0.5, "R5": 0.8, "R10": 1.0}
patterns = [".", "x", "\\"]#

# Configurazioni del grafico
labels = list(models["Resnet_50"].keys())  # Dataset source
models_keys = list(models.keys())
targets = list(base_colors.keys())
bar_width = 0.2
group_width = bar_width * len(targets) * len(models_keys)
start_pos = 0

x_positions = []
x_ticks_labels = []
grouped_data = {metric: [] for metric in metrics.keys()}

# Organizzazione dei dati
for label_idx, label in enumerate(labels):
    for model_idx, model in enumerate(models_keys):
        dataset = models[model][label]
        for target_idx, target in enumerate(targets):
            x_pos = start_pos + model_idx * len(targets) * bar_width + target_idx * bar_width
            for metric_name, metric_offset in metrics.items():
                metric_pos = target_indices[target][0] + metric_offset
                value = dataset[metric_pos]
                grouped_data[metric_name].append((x_pos, value, base_colors[target], patterns[model_idx]))
    x_ticks_labels.append(label)
    start_pos += group_width + 0.3  # Spazio tra i gruppi

# Plot
fig, ax = plt.subplots(figsize=(14, 6))
bottom_positions = {pos: 0 for pos in range(len(grouped_data["R1"]))}

# Creazione del grafico
for metric_name, data in grouped_data.items():
    for idx, (x_pos, value, base_color, pattern) in enumerate(data):
        color = mcolors.to_rgba(base_color, metric_shades[metric_name])
        ax.bar(
            x_pos,
            value,
            bar_width,
            color=color,
            edgecolor="darkslategray",
            hatch=pattern,
            bottom=bottom_positions[idx],
            label=f"{metric_name} - {targets[idx % len(targets)]}" if idx < len(targets) * len(models_keys) else None
        )
        bottom_positions[idx] += value

# Creazione della legenda
model_handles = [plt.Line2D([0], [0], color='darkslategray', lw=2, linestyle='None', marker=marker, markerfacecolor='gray', markeredgewidth=2, label=f"{model} Pattern{i}") for i, (model, marker) in enumerate(zip(models_keys, patterns))]
legend2 = ax.legend(model_handles, models_keys, title="Models", bbox_to_anchor=(1.05, 0.5), loc='upper left')
ax.add_artist(legend2)

handles, labels = ax.get_legend_handles_labels()
unique_labels = {label: handle for label, handle in zip(labels, handles)}
legend1 = ax.legend(unique_labels.values(), unique_labels.keys(), title="Legend", bbox_to_anchor=(1.05, 1), loc='upper left')

# Personalizzazione dell'asse X
x_ticks = [
    i * (group_width + 0.3) + group_width / 2 - bar_width * len(targets)
    for i in range(len(x_ticks_labels))
]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_ticks_labels, rotation=45)
ax.set_ylabel("Valori delle metriche")
ax.set_title("Metriche R1, R5 e R10 per Dataset Source, Modello e Target")

plt.tight_layout()
plt.show()



# # Colori per le metriche e target
# base_colors = {"Market": "blue", "Duke": "orange", "MSMT": "green"}
# metric_shades = {"R1": 0.6, "R5": 0.8, "R10": 1.0}
# patterns = ["//", "xx", "\\\\"]  # Pattern per i modelli
#
# # Configurazioni del grafico
# labels = list(models["Resnet_50"].keys())  # Dataset source
# models_keys = list(models.keys())
# targets = list(base_colors.keys())
# bar_width = 0.2
# group_width = bar_width * len(targets) * len(models_keys)
# start_pos = 0
#
# x_positions = []
# x_ticks_labels = []
# grouped_data = {metric: [] for metric in metrics.keys()}
#
# # Organizzazione dei dati
# for label_idx, label in enumerate(labels):
#     for model_idx, model in enumerate(models_keys):
#         dataset = models[model][label]
#         for target_idx, target in enumerate(targets):
#             x_pos = start_pos + model_idx * len(targets) * bar_width + target_idx * bar_width
#             for metric_name, metric_offset in metrics.items():
#                 metric_pos = target_indices[target][0] + metric_offset
#                 value = dataset[metric_pos]
#                 if metric_name != "R1":
#                     prev_metric_name = list(metrics.keys())[list(metrics.keys()).index(metric_name) - 1]
#                     prev_value = dataset[target_indices[target][0] + metrics[prev_metric_name]]
#                     value = value - prev_value
#                 grouped_data[metric_name].append((x_pos, value, base_colors[target], patterns[model_idx]))
#     x_ticks_labels.append(label)
#     start_pos += group_width + 0.3  # Spazio tra i gruppi
#
# # Plot
# fig, ax = plt.subplots(figsize=(14, 6))
# bottom_positions = {pos: 0 for pos in range(len(grouped_data["R1"]))}
#
# # Creazione del grafico
# for metric_name, data in grouped_data.items():
#     for idx, (x_pos, value, base_color, pattern) in enumerate(data):
#         color = mcolors.to_rgba(base_color, metric_shades[metric_name])
#         ax.bar(
#             x_pos,
#             value,
#             bar_width,
#             color=color,
#             edgecolor="black",
#             hatch=pattern,  # Applicazione del pattern
#             bottom=bottom_positions[idx],
#             label=f"{metric_name} - {targets[idx % len(targets)]}" if idx < len(targets) * len(models_keys) else None
#         )
#         bottom_positions[idx] += value
#
# # Creazione della legenda per le metriche
# handles, labels = ax.get_legend_handles_labels()
# unique_labels = {label: handle for label, handle in zip(labels, handles)}
# ax.legend(unique_labels.values(), unique_labels.keys(), title="Metriche", bbox_to_anchor=(1.05, 1), loc='upper left')
#
# # Creazione della legenda separata per i modelli
# model_handles = [plt.Line2D([0], [0], color='gray', lw=2, linestyle='None', marker='o', markerfacecolor='gray', markeredgewidth=2, label=model) for model in models_keys]
# ax.legend(model_handles, models_keys, title="Modelli", bbox_to_anchor=(1.05, 0.5), loc='upper left')
#
# # Personalizzazione dell'asse X
# x_ticks = [
#     i * (group_width + 0.3) + group_width / 2 - bar_width * len(targets)
#     for i in range(len(x_ticks_labels))
# ]
# ax.set_xticks(x_ticks)
# ax.set_xticklabels(x_ticks_labels, rotation=45)
# ax.set_ylabel("Valori delle metriche")
# ax.set_title("Metriche R1, R5 e R10 per Dataset Source, Modello e Target")
#
# plt.tight_layout()
# plt.show()
