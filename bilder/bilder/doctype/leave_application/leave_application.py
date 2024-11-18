import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from datetime import timedelta

class LeaveApplication(Document):
    def validate(self):
        # Check if both start_date and end_date are provided
        if self.start_date and self.end_date:
            # Convert start_date and end_date to date objects
            start_date = getdate(self.start_date)
            end_date = getdate(self.end_date)

            # Ensure end_date is not earlier than start_date
            if end_date < start_date:
                frappe.throw("End Date cannot be earlier than Start Date")

            # Calculate total leave days excluding Sundays
            self.total_days = self.calculate_leave_days(start_date, end_date)
        else:
            frappe.throw("Please provide both Start Date and End Date")

    def calculate_leave_days(self, start_date, end_date):
        """
        Calculate total leave days excluding Sundays between start_date and end_date.
        """
        total_days = 0
        current_date = start_date

        while current_date <= end_date:
            if current_date.weekday() != 6:  # 6 represents Sunday
                total_days += 1
            current_date += timedelta(days=1)

        return total_days

