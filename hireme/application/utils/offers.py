from datetime import datetime

class Offers(object):
    """
    This class is used to store
    data regarding job offers.
    """
    listings = []

    def append_offer(self, form):
        """
        Appends the details of the job offer
        to this object's list variable termed 'listings'.
        The data used is extracted from the contact form
        upon user submission.
        :param form: contact form
        :return:
        """
        today = datetime.today()
        self.listings.append({
            'job_title': form.job_title.data,
            'company': form.recruiter_company.data,
            'time': today.strftime("%a %b %y")
        })