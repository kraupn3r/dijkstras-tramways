from django.db import models


class Line(models.Model):
    number = models.PositiveIntegerField()
    first_stop = models.ForeignKey(
        'tramstop', on_delete=models.PROTECT, related_name="startinglines", null=True)
    last_stop = models.ForeignKey(
        'tramstop', on_delete=models.PROTECT, related_name="endinglines", null=True)
    walkline = models.BooleanField(default=False)

    def __str__(self):
        return "{}, direction {}".format(self.number, self.last_stop)


class TramStop(models.Model):
    name = models.CharField(max_length=40)
    stopid = models.PositiveIntegerField(default=0)
    stopnumber = models.PositiveIntegerField()
    line = models.ManyToManyField(Line, related_name="stops")
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)

    class Meta:
        unique_together = ('name', 'stopnumber')

    def __str__(self):
        return "{} {}".format(self.name, self.view_number)

    @property
    def view_number(self):
        return str(self.stopnumber).zfill(2)


class StopTimetable(models.Model):
    line = models.ForeignKey(
        Line, on_delete=models.CASCADE, related_name='stoptables')
    stop = models.ForeignKey(
        TramStop, on_delete=models.CASCADE, related_name='stoptables')
    timearray = models.TextField()

    class Meta:
        unique_together = ('line', 'stop')


class LineTimetable(models.Model):
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    stop = models.ForeignKey(TramStop, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    time_since_0 = models.PositiveIntegerField()

    def __str__(self):
        return "{} {} {} {}".format(self.line.number, self.stop.name, self.order, self.time_since_0)


class AdjacencyMatrixCell(models.Model):
    col = models.ForeignKey(
        TramStop, on_delete=models.CASCADE, related_name='colstop')
    row = models.ForeignKey(
        TramStop, on_delete=models.CASCADE, related_name='rowstop')
    value = models.PositiveIntegerField()
    lines = models.ManyToManyField(Line)

    class Meta:
        unique_together = ('col', 'row')
        verbose_name_plural = 'Adjacency Matrices'

    def __str__(self):
        return "{} {} {} {}".format(self.col, self.row, self.value, self.lines.count())


class AdjacencyMatrix(models.Model):
    matrix = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_at'


class LineMatrix(models.Model):
    matrix = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created_at'
        verbose_name_plural = 'Line Matrices'
