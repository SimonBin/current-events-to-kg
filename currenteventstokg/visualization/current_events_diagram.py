# Copyright: (c) 2022, Lars Michaelis
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from os import makedirs
import locale
from typing import Dict, List, Optional, Tuple, Union
import json
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from currenteventstokg import currenteventstokg_dir
from currenteventstokg.etc import month2int, months

from .current_events_graph import CurrentEventsGraphSplit, CurrentEventsGraphABC

class Diagram():
    def __init__(self, sub_dir_name:str, diagram_name:str):
        self.filename = diagram_name

        self.cache_dir = currenteventstokg_dir / "cache" / sub_dir_name
        makedirs(self.cache_dir, exist_ok=True)

        self.diagrams_dir = currenteventstokg_dir / "diagrams/" / sub_dir_name
        makedirs(self.diagrams_dir, exist_ok=True)

    def _load_json(self, file_path):
        with open(file_path, mode='r', encoding="utf-8") as f:
            return json.load(f)
    
    def _dump_json(self, file_path, obj):
        with open(file_path, mode='w', encoding="utf-8") as f:
            json.dump(obj, f)
    
    def _create_bar_chart_per_month(self, data, title:str, x_label:str, y_label:str):
        fig, ax = plt.subplots(constrained_layout=True)
        
        keys = sorted(list(data.keys()))
        x,y = [],[]
        for year in keys:
            for month in range(12):
                if not np.isnan(data[year][month]):
                    y.append(data[year][month])
                    x.append(datetime.datetime(int(year), month+1, 1))
                    
        locale.setlocale(locale.LC_TIME,'en_US.UTF-8')
        
        if len(keys) > 1:
            # multiple years span
            locator = mdates.AutoDateLocator() #minticks=3, maxticks=7
            locator.intervald[mdates.MONTHLY] = [4]
            ax.xaxis.set_major_locator(locator)
            formatter = mdates.ConciseDateFormatter(locator)
            ax.xaxis.set_major_formatter(formatter)
            
            minor_locator = mdates.MonthLocator()
            ax.xaxis.set_minor_locator(minor_locator)
        else:
            locator = mdates.MonthLocator()
            formatter = mdates.ConciseDateFormatter(locator, show_offset=False)

            ax.xaxis.set_major_locator(locator)
            ax.xaxis.set_major_formatter(formatter)

            ax.minorticks_off()

        ax.bar(x, y,
            width=25
        )
        ax.set_title(title)
        ax.set_ylabel(f"\\textbf{{{y_label}}}")
        ax.set_xlabel(f"\\textbf{{{x_label}}}")
        
        return fig


    def _create_bar_chart_from_data(self, ax, data, title:str, x_label:str, y_label:str):        
        x = list(data.keys())
        y = [data[key] for key in x]

        ax.bar(x, y, 
            # color=None,
            # edgecolor="black",
        )
        ax.set_title(title)
        ax.set_ylabel(f"\\textbf{{{y_label}}}")
        ax.set_xlabel(f"\\textbf{{{x_label}}}")

class CurrentEventDiagram(Diagram):
    def __init__(self, sub_dir_name:str, graph_names:List[str], graph_modules=["base"], graph_class:CurrentEventsGraphABC=CurrentEventsGraphSplit):
        self.graph_names = graph_names # need to be sorted with first one first!
        self.graph_class = graph_class

        diagram_name = f"{self.graph_names[0]}_{self.graph_names[-1]}"
        super().__init__(sub_dir_name, diagram_name)

        self._load_graph(graph_names, graph_modules)
    
    def _load_graph(self, graph_names, graph_modules):
        self.graph = self.graph_class(graph_names=graph_names, graph_modules=graph_modules)


class CurrentEventBarChart(CurrentEventDiagram):
    def __init__(self, sub_dir_name:str, graph_names:List[str], graph_modules=["base"], graph_class:CurrentEventsGraphABC=CurrentEventsGraphSplit):
        super().__init__(sub_dir_name, graph_names, graph_modules, graph_class)

    
