import app


class approveAPI():
    def __init__(self):
        self.approve_url = app.BASE_URL + '/member/realname/approverealname'
        self.getapprove_url = app.BASE_URL + '/member/member/getapprove'

    def approve(self, session, realname, cardID):
        data = {"realname": realname,
                "card_id": cardID}
        response = session.post(self.approve_url, data=data, files={"x": "y"})
        return response

    def getAPProve(self,session):
        response = session.post(self.getapprove_url)
        return response

