from wisdoms.config import c
from wisdoms.ms import ms_base, permit


ES_HOST = c.get('ES_HOST')
MS_HOST = c.get('MS_HOST')

MsBase = ms_base(MS_HOST, name='', entrance='', entrance4app='', roles=[], types='free')
auth_ = permit(MS_HOST)
