from datetime import datetime

class Offers(object):
    listings = []

    def append_offer(self, form):
        today = datetime.today()
        self.listings.append({
            'job_title': form.job_title.data,
            'company': form.recruiter_company.data,
            'time': today.strftime("%a %b %y")
        })