from gemini.models.views.sensor_records_immv import SensorRecordsIMMVModel

number_of_pages, records = SensorRecordsIMMVModel.paginate(
    order_by="timestamp",
    page_number=10000,
    page_limit=100
)

print(f"Number of pages: {number_of_pages}")