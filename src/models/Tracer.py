from PySide2.QtCore import QObject, Property, Slot, Signal
from PySide2 import QtCore

import pyautogui
import time
from timeit import default_timer

from .Trace import Trace
from .TraceListModel import TraceListModel

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

class Tracer(QObject):
    progress_changed = Signal(float)
    delay_changed = Signal(int)

    def __init__(self, solver, preview, matrix):
        super().__init__()
        self._delay_ms = 35
        self.solver = solver
        self.preview = preview
        self.matrix = matrix

        self.trace_list = TraceListModel()

        self._progress = 0.0

        self.running = False

    def calculate_traces(self):
        results = self.solver.calculate_results(self.matrix)
        traces = []
        for result in results:
            trace = Trace(result)
            traces.append(trace)
        self.traces = traces
        self.progress = 0.0


    def start(self):
        coordinates = self.preview.get_coordinates()
        unsolved_traces = []
        for index, trace in enumerate(self.traces):
            if not trace.is_complete:
                unsolved_traces.append((index, trace))

        solved_traces = 0

        self.running = True

        for index, trace in unsolved_traces:
            for i, position in enumerate(trace.path):
                if not self.running:
                    return

                coordinate = coordinates[position]
                x, y = coordinate
                pyautogui.moveTo(x, y)

                if i == 0:
                    pyautogui.mouseDown()

                time.sleep(self.delay_ms / 1000)
            
            pyautogui.mouseUp()
            solved_traces += 1

            total_traces = len(self.traces)
            incomplete_traces = len(unsolved_traces) - solved_traces
            self.progress = incomplete_traces / total_traces 

            trace.is_complete = True

        self.running = False

    @property
    def progress(self):
        return self._progress
    
    @progress.setter
    def progress(self, progress):
        self._progress = progress
        self.progress_changed.emit(progress)
    
    @Property(int, notify=delay_changed)
    def delay_ms(self):
        return self._delay_ms
    
    @Slot(int)
    def set_delay_ms(self, delay_ms):
        self._delay_ms = delay_ms
        self.delay_changed.emit(delay_ms)

    @property
    def traces(self):
        return self.trace_list.traces
    
    @traces.setter
    def traces(self, traces):
        self.trace_list.traces = traces

                








