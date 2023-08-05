from django.db import models
from django.utils.timezone import now


class ManagementCommandLog(models.Model):

    """Records the running of a management command."""

    app_name = models.CharField(
        help_text="The app containing the management command", max_length=100
    )
    command_name = models.CharField(
        help_text="The management command that was executed", max_length=100
    )
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    exit_code = models.IntegerField(
        default=None,
        help_text="0 if the command ran without error.",
        null=True,
        blank=True,
    )
    output = models.TextField(
        help_text="The output of the command (stored as a string)",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.management_command} run at {self.started_at}"

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.pk} command="{self.management_command}">'

    @property
    def management_command(self):
        return f"{self.app_name}.{self.command_name}"

    @property
    def duration(self):
        try:
            return self.finished_at - self.started_at
        except TypeError:
            return None

    def start(self):
        """Mark the beginning of a management command execution."""
        if any([self.started_at, self.finished_at, self.output, self.exit_code]):
            raise ValueError("Log object is already in use.")
        self.started_at = now()
        self.save()

    def stop(self, *, output, exit_code):
        """Mark the end of a management command execution."""
        if not self.started_at:
            raise ValueError("Log object has not been started.")
        if any([self.finished_at, self.output, self.exit_code]):
            raise ValueError("Log object has already completed.")
        self.finished_at = now()
        self.output = output
        self.exit_code = exit_code
        self.save()
