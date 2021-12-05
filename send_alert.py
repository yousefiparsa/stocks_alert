import os
import re

import asyncio
from email.message import EmailMessage
from typing import Collection, List, Tuple, Union

import aiosmtplib

HOST = 'smtp.gmail.com'
CARRIER_MAP = {
    'verizon': 'vtext.com',
    'tmobile': 'tmomail.net',
    'sprint': 'messaging.sprintpcs.com',
    'at&t': 'txt.att.net',
    'boost': 'smsmyboostmobile.com',
    'cricket': 'sms.cricketwireless.net',
    'uscellular': 'email.uscc.net',
}

async def send_txt(
    num: Union[str, int],
    carrier: str,
    email: str,
    pword: str,
    msg: str,
    subj: str
) -> Tuple[dict, str]:
    to_email = CARRIER_MAP[carrier]

    # build message
    message = EmailMessage()
    message['From'] = 'stocks_alert_{}'.format(email)
    message['To'] = f'{num}@{to_email}'
    message['Subject'] = subj
    message.set_content(msg)

    # send
    send_kws = dict(username=email, password=pword, hostname=HOST, port=587, start_tls=True)
    res = await aiosmtplib.send(message, **send_kws)  # type: ignore
    msg = 'Failed' if not re.search(r"\sOK\s", res[1]) else 'Succeeded'
    print(msg)
    print(res)
    return res


async def send_txts(
    nums: Collection[Union[str, int]],
    carrier: str,
    email: str,
    pword: str,
    msg: str,
    subj: str
) -> List[Tuple[dict, str]]:
    tasks = [send_txt(n, carrier, email, pword, msg, subj) for n in set(nums)]
    return await asyncio.gather(*tasks)


if __name__ == "__main__":
    _num = os.environ.get('NUM')
    _carrier = os.getenv(key='CARRIER')
    _email = os.getenv(key='EMAIL')
    _pword = os.getenv(key='PWORD')
    _msg = 'Stocks alert test'
    _subj = 'Stocks Alert'
    coro = send_txt(_num, _carrier, _email, _pword, _msg, _subj)
    asyncio.run(coro)
