from django.contrib import admin


from .models import Line, TramStop, AdjacencyMatrix, LineMatrix, StopTimetable, LineTimetable,AdjacencyMatrixCell,LineMatrixCell
# Register your models here.
admin.site.register(Line)
admin.site.register(TramStop)
admin.site.register(AdjacencyMatrix)
admin.site.register(LineMatrix)
admin.site.register(StopTimetable)
admin.site.register(LineTimetable)
admin.site.register(AdjacencyMatrixCell)
admin.site.register(LineMatrixCell)
