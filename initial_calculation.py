from Deadline import DeadlineConnect

WEB_SERVICE_IP = "0.0.0.0"
WEB_SERVICE_PORT = 0000
EXTRA_INFO_FIELD = "Ex0"
CURRENCY = "EUR"
PRICE_PER_RENDER_HOUR = 0.26

deadline_connection = DeadlineConnect.DeadlineCon(WEB_SERVICE_IP, WEB_SERVICE_PORT)

for job in deadline_connection.Jobs.GetJobs():
    job_id = job["_id"]
    render_time = deadline_connection.Jobs.GetJobDetails(job_id)[job_id]["Statistics"][
        "Total Task Render Time"
    ]

    days, hours, minutes, seconds = [int(part) for part in render_time.split(":")]
    total_hours = days * 24 + hours + minutes / 60 + seconds / 3600
    total_cost = round(total_hours * 0.26, 2)

    job["Props"][EXTRA_INFO_FIELD] = f"{total_cost} EUR"
    deadline_connection.Jobs.SaveJob(job)
