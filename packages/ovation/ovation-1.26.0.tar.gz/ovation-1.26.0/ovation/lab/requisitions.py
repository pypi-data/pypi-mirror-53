from ovation.lab.constants import REQUISITIONS

API_V3 = '/api/v3'


# def get_requisitions(session):  # TODO add filters
#     s3 = session.with_prefix(API_V3)
#     return s3.get(s3.path(REQUISITIONS, include_org=False))

def get_requisition(session, requisition_id):
    s3 = session.with_prefix(API_V3)
    return s3.get(s3.path(REQUISITIONS, id=requisition_id, include_org=False))
