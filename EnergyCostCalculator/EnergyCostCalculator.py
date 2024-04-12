"""A simple Deadline event plugin to calculate render costs.
Written by Mervin van Brakel, 2024."""

from Deadline.Events import DeadlineEventListener
from Deadline.Scripting import RepositoryUtils


def GetDeadlineEventListener():
    """Gets called by Deadline to initiate the event plugin."""
    return EnergyCostCalculator()


def CleanupDeadlineEventListener(eventListener):
    """Gets called by Deadline to cleanup the event plugin."""
    eventListener.Cleanup()


class EnergyCostCalculator(DeadlineEventListener):
    def __init__(self):
        """Sets up callbacks and imports config."""
        self.OnJobFinishedCallback += self.OnJobFinished
        self.OnSlaveRenderingCallback += self.OnSlaveRendering
        self.config = RepositoryUtils.GetEventPluginConfig("EnergyCostCalculator")

    def Cleanup(self):
        """Runs when this event plugins gets cleared."""
        del self.OnJobFinishedCallback
        del self.OnSlaveRenderingCallback

    def OnJobFinished(self, job):
        """Runs when a job finishes."""
        self.calculate_costs(job)

    def OnSlaveRendering(self, _, job):
        """Runs when a worker starts rendering."""
        self.calculate_costs(job)

    def calculate_costs(self, job):
        """Calculates the job cost based on render hour price setting.

        Args:
            job: Render farm job
        """
        job_details = RepositoryUtils.GetJobDetails([job])
        render_time = job_details[job.JobId]["Statistics"]["Total Task Render Time"]

        days, hours, minutes, seconds = [float(part) for part in render_time.split(":")]
        total_hours = days * 24 + hours + minutes / 60 + seconds / 3600

        total_cost = round(
            total_hours * float(self.config.GetConfigEntry("CostPerRenderHour")), 2
        )
        currency_string = self.config.GetConfigEntry("CurrencyString")

        job = self.get_job_with_extra_info_field(job, f"{total_cost} {currency_string}")
        RepositoryUtils.SaveJob(job)

    def get_job_with_extra_info_field(self, job, data):
        """Sets the correct extra info field based on the config

        Args:
            job: The job we will set the data on
            data: The data to set

        Returns:
            The job with the extra info field set
        """
        extra_info_to_set = int(self.config.GetConfigEntry("ExtraInfoField"))
        if not 0 <= extra_info_to_set <= 9:
            raise ValueError("The extra info field must be set between 0 and 9.")

        attribute_name = f"JobExtraInfo{extra_info_to_set}"
        setattr(job, attribute_name, data)
        return job
