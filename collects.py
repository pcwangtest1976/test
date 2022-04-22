# -*- coding: UTF-8 -*-
import traceback

class collect():

    def __init__(self):

        pass

    def get_result(self, summary=None):
        '''
        get result from summary
        '''
        if summary==None:
            summary={}
        result = {}
        # print('summary=',summary)
        # print('summary type',type(summary))
        try:
            # summary is dict type
            if isinstance(summary,dict) and isinstance(summary['details'],list) and isinstance(summary['details'][0],dict):
                result['stat'] = summary['details'][0]['stat']
                result['records'] = summary['details'][0]['records']
                result['success'] = summary['details'][0]["success"]
            else:
                result['stat']=None
                result['records']=None
                result['success']=None
                raise('can not get result for summary=',summary)
            # print('get - result==',result)
            return result
        except Exception as e:
            traceback.print_exc()
            print ('can not get result for :' + str(result))
            raise ('exception =',e)
        except BaseException as e:
            traceback.print_exc()
            raise ('execption =', e)
        except:
            return None

    def get_request(self, result=None):

        if result==None:
            result={}
        return request().get_request(result)

    def get_response(self, result=None):

        if result==None:
            result={}
        return response().get_response(result)


class request():

    def __init__(self):

        pass

    def get_request(self, result=None):
        '''
        get request
        '''
        if result==None:
            result={}
        try:
            if result != None and isinstance(result, dict) and isinstance(result['records'], list):
                request = result['records'][0]['meta_datas']['data'][0]['request']
                return request
            else:
                return None
        except Exception as e:
            traceback.print_exc()
            print('can not get result for :' + str(result))
            raise ('exception =' , e)
        except BaseException as e:
            traceback.print_exc()
            raise ('execption =', e)
        except:
            return None

    def get_request_info(self, result=None, info_name=''):
        '''
        get request key's info
        '''
        if result==None:
            result={}
        try:
            request = self.get_request(result)
            if request != None:
                return request[result]
            else:
                return None
        except Exception as e:
            traceback.print_exc()
            print ('can not get response for ' + str(result) + ' ' + info_name)
            raise ('exception =' ,e)
        except BaseException as e:
            traceback.print_exc()
            raise ('execption =', e)
        except:
            return None


    def get_request_url(self, result='', info_name='url'):
        '''
        get request url
        '''
        if result==None:
            result={}
        return self.get_request_info(result, info_name)

    def get_request_method(self, result=None, info_name='method'):
        '''
        get request method
        '''
        if result==None:
            result={}
        return self.get_request_info(result, info_name)

    def get_request_headers(self, result=None, info_name='headers'):
        '''
        get request header
        '''
        if result==None:
            result={}
        return self.get_request_info(result, info_name)

    def get_request_status_code(self, result=None, info_name='status_code'):
        '''
        get request status code
        '''
        if result==None:
            result={}
        return self.get_request_info(result, info_name)

    def get_request_cookies(self, result=None, info_name='cookies'):
        '''
        get request cookies
        '''
        if result==None:
            result={}
        return self.get_request_info(result, info_name)

    def get_request_body(self, result=None, info_name='body'):
        '''
        get request body
        '''
        if result==None:
            result={}
        return self.get_request_info(result, info_name)

    def get_request_stat(self, result=None, info_name='stat'):
        '''
        get request stat
        '''
        if result==None:
            result={}
        return self.get_request_info(result, info_name)

    def get_request_validators(self, result=None, info_name='validators'):
        '''
        get request validators
        '''
        if result==None:
            result={}
        return self.get_request_info(result, info_name)


class response():

    def __init__(self):

        self.result = ''

    def get_response(self, result=None):
        '''
        get response
        '''
        if result==None:
            result={}
        try:
            if result != None and isinstance(result, dict) and isinstance(result['records'], list):
                response = result['records'][0]['meta_datas']['data'][0]['response']
                return response
            else:
                return None
        except Exception as e:
            traceback.print_exc()
            print ('can not get result for :' + str(result))
            raise ('exception =',e)
        except BaseException as e:
            traceback.print_exc()
            raise ('execption =', e)
        except:
            return None

    def get_response_info(self, result=None, info_name=''):
        '''
        get response info by key
        '''
        if result==None:
            result={}
        try:
            response = self.get_response(result)
            if response != None:
                return response[info_name]
            else:
                return None
        except Exception as e :
            traceback.print_exc()
            print ('can not get response for ' + str(result) + ' ' + info_name)
            raise ('exception =',e )
        except BaseException as e:
            traceback.print_exc()
            raise ('execption =', e)
        except:
            return None

    def get_response_url(self, result=None, info_name='url'):
        '''
        get response url
        '''
        if result==None:
            result={}
        return self.get_response_info(result, info_name)

    def get_response_method(self, result=None, info_name='method'):
        '''
        get response method
        '''
        if result==None:
            result={}
        return self.get_response_info(result, info_name)

    def get_response_headers(self, result=None, info_name='headers'):
        '''
        get response header
        '''
        if result==None:
            result={}
        return self.get_response_info(result, info_name)

    def get_response_status_code(self, result=None, info_name='status_code'):
        '''
        get response status code
        '''
        if result==None:
            result={}
        return self.get_response_info(result, info_name)

    def get_response_cookies(self, result=None, info_name='cookies'):
        '''
        get response cookies
        '''
        if result==None:
            result={}
        return self.get_response_info(result, info_name)

    def get_response_body(self, result=None, info_name='body'):
        '''
        get response body
        '''
        if result==None:
            result={}
        return self.get_response_info(result, info_name)

    def get_response_stat(self, result=None, info_name='stat'):
        '''
        get response stat
        '''
        if result==None:
            result={}
        return self.get_response_info(result, info_name)

    def get_response_validators(self, result=None, info_name='validators'):
        '''
        get response validatoers
        '''
        if result==None:
            result={}
        return self.get_response_info(result, info_name)


if __name__ == "__main__":

    pass
