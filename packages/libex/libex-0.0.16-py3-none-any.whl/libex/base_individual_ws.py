#!/usr/bin/env python3

import asyncio

import logging
import logging.handlers
import websockets
                
import traceback

from .common.timer import Timer

logger = logging.getLogger(__name__)
 

class BaseIndividualWs(object):
    """记录程序，将各交易所的实时行情数据初步解析后记录成文件"""

    def __init__(self,exchange ,symbols ,secrets,listener):
        super(BaseIndividualWs, self).__init__()
        
        self._exchange = exchange
        
        self._symbols = symbols
        self._secrets = secrets

        self._listener = listener

    def run_task(self):
        try:
            asyncio.get_event_loop().run_until_complete(self.task())

        except Exception as e:
            logger.error( 'Adapter ERROR, %s ,%s' , e, traceback.format_exc() ) 

    async def task(self):

        # max run 3 times if connect exception 
        for i in range(0,3):

            try:
                await self.connect()

            except websockets.ConnectionClosed as e:
                logger.error(f"{self._exchange},connect closed,will reconnect,{e},{traceback.format_exc()}")
                
            except Exception as e:

                logger.error(traceback.format_exc())

                raise e

    def convert_trade(self,origin):
        """ 该方法需要子类实现 """
        pass

    def convert_book_snapshot(self,origin):
        """ 该方法需要子类实现 """
        pass

    def convert_book_update(self,origin):
        """ 该方法需要子类实现 """
        pass

    async def connect(self):    
        """ 该方法需要子类实现 """
        pass
