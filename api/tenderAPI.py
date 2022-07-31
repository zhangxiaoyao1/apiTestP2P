import app


class tenderAPI():
    def __init__(self):
        self.get_loaninfo_url = app.BASE_URL + "/common/loan/loaninfo"
        self.tender_url = app.BASE_URL + "/trust/trust/tender"
        self.tenderlist_url = app.BASE_URL + "/loan/tender/mytenderlist"

    def get_loaninfo(self, session, tender_id):
        data = {"id": tender_id}
        response = session.post(self.get_loaninfo_url, data=data)
        return response

    def tender(self, session, tender_id, amount):
        data = {"id": tender_id, "amount": amount}
        response = session.post(self.tender_url, data=data)
        return response

    def get_tenderlist(self, session, status):
        data = {"status": status}
        response = session.post(self.tenderlist_url, data=data)
        return response
