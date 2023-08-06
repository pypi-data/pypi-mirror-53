#
# documentation:
import requests
import json
import arrow
import urllib3

# Return codes expected by Nagios
OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

#Disable warnings https
urllib3.disable_warnings()

class HistorianChecks:
    def __init__(self, url, access_token, instance):
        
        #initial
        self.url = url
        self.access_token = access_token
        self.instance = instance

        #Declare vars for tags with instance
        self.STATUS_COM_010 = '{}'.format(self.instance) + '.STATUS_COM_010.F_CV'        
        self.STATUS_COM_073 = '{}'.format(self.instance) + '.STATUS_COM_073.F_CV'
        self.STATUS_COM_075 = '{}'.format(self.instance) + '.STATUS_COM_075.F_CV'
        self.STATUS_COM_079 = '{}'.format(self.instance) + '.STATUS_COM_079.F_CV'
        self.STATUS_COM_080 = '{}'.format(self.instance) + '.STATUS_COM_080.F_CV'
        self.STATUS_COM_110 = '{}'.format(self.instance) + '.STATUS_COM_110.F_CV'
        self.STATUS_COM_120 = '{}'.format(self.instance) + '.STATUS_COM_120.F_CV'
        self.STATUS_COM_130 = '{}'.format(self.instance) + '.STATUS_COM_130.F_CV'
        self.STATUS_COM_141 = '{}'.format(self.instance) + '.STATUS_COM_141.F_CV'
        self.STATUS_COM_142 = '{}'.format(self.instance) + '.STATUS_COM_142.F_CV'
        self.STATUS_COM_144 = '{}'.format(self.instance) + '.STATUS_COM_144.F_CV'
        self.STATUS_COM_148 = '{}'.format(self.instance) + '.STATUS_COM_148.F_CV'
        self.STATUS_COM_151 = '{}'.format(self.instance) + '.STATUS_COM_151.F_CV'
        self.STATUS_COM_152 = '{}'.format(self.instance) + '.STATUS_COM_152.F_CV'
        self.STATUS_COM_155 = '{}'.format(self.instance) + '.STATUS_COM_155.F_CV'
        self.STATUS_COM_160 = '{}'.format(self.instance) + '.STATUS_COM_160.F_CV'
        self.STATUS_COM_192 = '{}'.format(self.instance) + '.STATUS_COM_192.F_CV'
        self.STATUS_COM_193 = '{}'.format(self.instance) + '.STATUS_COM_193.F_CV'
        self.STATUS_SAC_CYCLES_SEC = '{}'.format(self.instance) + '.STATUS_SAC_CYCLES_SEC.F_CV'
        self.STATUS_SAC_OVERRUNS = '{}'.format(self.instance) + '.STATUS_SAC_OVERRUNS.F_CV'
        self.STATUS_SAC_STATUS = '{}'.format(self.instance) + '.STATUS_SAC_STATUS.F_CV'
        self.STATUS_WS_ACTIVE_SESSIONS = '{}'.format(self.instance) + '.STATUS_WS_ACTIVE_SESSIONS.F_CV'
        self.STATUS_WS_CLIENT_CONNECTIONS = '{}'.format(self.instance) + '.STATUS_WS_CLIENT_CONNECTIONS.F_CV'
        self.STATUS_WS_HOST_CONNECTIONS = '{}'.format(self.instance) + '.STATUS_WS_HOST_CONNECTIONS.F_CV'
        self.STATUS_WS_MAXIMUM_SESSIONS = '{}'.format(self.instance) + '.STATUS_WS_MAXIMUM_SESSIONS.F_CV'
        self.STATUS_WS_SERVICE = '{}'.format(self.instance) + '.STATUS_WS_SERVICE.F_CV'
        self.STATUS_LAST_UPDATE = '{}'.format(self.instance) + '.STATUS_LAST_UPDATE.A_CV'

    def get_tags_data(self):
    

        # Request JSON machines
        #headers = {'accept': 'application/json'}
        header_token = {"Authorization": "Bearer {}".format(self.access_token)}

        #Add tags to the URL
        url = '{}'.format(self.url) + ';' +'{}'.format(self.STATUS_COM_010) + ';' +'{}'.format(self.STATUS_COM_073) + ';' +'{}'.format(self.STATUS_COM_075) + ';' +'{}'.format(self.STATUS_COM_079) + ';' +'{}'.format(self.STATUS_COM_080) + ';' +'{}'.format(self.STATUS_COM_110) + ';' +'{}'.format(self.STATUS_COM_120) + ';' +'{}'.format(self.STATUS_COM_130) + ';' +'{}'.format(self.STATUS_COM_141) + ';' +'{}'.format(self.STATUS_COM_142) + ';' +'{}'.format(self.STATUS_COM_144) + ';' +'{}'.format(self.STATUS_COM_148) + ';' +'{}'.format(self.STATUS_COM_151) + ';' +'{}'.format(self.STATUS_COM_152) + ';' +'{}'.format(self.STATUS_COM_155) + ';' +'{}'.format(self.STATUS_COM_160) + ';' +'{}'.format(self.STATUS_COM_192) + ';' +'{}'.format(self.STATUS_COM_193) + ';' +'{}'.format(self.STATUS_SAC_CYCLES_SEC) + ';' +'{}'.format(self.STATUS_SAC_OVERRUNS) + ';' +'{}'.format(self.STATUS_SAC_STATUS) + ';' +'{}'.format(self.STATUS_WS_ACTIVE_SESSIONS) + ';' +'{}'.format(self.STATUS_WS_CLIENT_CONNECTIONS) + ';' +'{}'.format(self.STATUS_WS_HOST_CONNECTIONS) + ';' +'{}'.format(self.STATUS_WS_MAXIMUM_SESSIONS) + ';' +'{}'.format(self.STATUS_WS_SERVICE) + ';' +'{}'.format(self.STATUS_LAST_UPDATE) 

        # requests doc http://docs.python-requests.org/en/v0.10.7/user/quickstart/#custom-headers
        r = requests.get(url=url, headers=header_token, verify=False)

        return r.json(), r.status_code
    
    def check_tags_data(self):

        #Vars
        retrcode = OK
		#retrcodetag = OK

        #Create tuple with json and status code
        historian_tuple = self.get_tags_data()

        #Get data tags from tuple
        historian_data = historian_tuple[0]  


        perfdata_list = ['{}'.format(self.STATUS_SAC_CYCLES_SEC), '{}'.format(self.STATUS_WS_ACTIVE_SESSIONS), 
                        '{}'.format(self.STATUS_SAC_OVERRUNS), '{}'.format(self.STATUS_WS_CLIENT_CONNECTIONS)]
        
        tags_max_value = {'{}'.format(self.STATUS_SAC_OVERRUNS): 10}

        tags_warn_value = {'{}'.format(self.STATUS_SAC_OVERRUNS): 5}

        msgdata = ''
        msgerror = ''
        retrperfdata = ''
        retrmsg = ''

        #Validate Data
        for i, val in enumerate(historian_data['Data']):
            retrcodetag = OK
            ErrorCode = val.get('ErrorCode', 1)
            TagName = val.get('TagName', '')
            Samples = val.get('Samples', [])
            SamplesN = 0
            
            msgdata += 'Tag: {}, ErrorCode: {} \n'.format(val.get('TagName'), ErrorCode)

            #Validate ErrorCode (0 = Ok)
            if ErrorCode != 0:
                retrcode = CRITICAL
                retrcodetag = CRITICAL

            #Validate Samples
            for x, vsample in enumerate(Samples):
                
                #Def Vars
                SamplesN += 1
                Quality = vsample.get('Quality', 0)
                TimeStamp = vsample.get('TimeStamp', '')
                Value = vsample.get('Value')                
                actual_time = arrow.get()

                msgdata += 'SampleN: {}, Quality: {}, TimeStamp: {}, Value: {} \n'.format(SamplesN, Quality, TimeStamp, Value)
                
                if TagName in perfdata_list:
                    retrperfdata += '{}={};{};{};; '.format(TagName, Value, tags_warn_value.get(TagName, ''), tags_max_value.get(TagName, ''))
                
                #Validate Quality (0 – Bad,  1 – Uncertain, 2 – NA , 3 – Good)
                if Quality != 3:
                    retrcode = CRITICAL
                    retrcodetag = CRITICAL

                #Validate Value (0 = Ok) 
                if not TagName in [self.STATUS_SAC_STATUS , self.STATUS_WS_SERVICE, self.STATUS_SAC_CYCLES_SEC, self.STATUS_SAC_OVERRUNS, self.STATUS_WS_ACTIVE_SESSIONS , self.STATUS_WS_CLIENT_CONNECTIONS , self.STATUS_WS_HOST_CONNECTIONS , self.STATUS_WS_MAXIMUM_SESSIONS, self.STATUS_LAST_UPDATE]:   
                    if Value != '0':
                        retrcode = CRITICAL
                        retrcodetag = CRITICAL

                #STATUS_SAC_STATUS / STATUS_WS_SERVICE - ( 0=STOP | 1=RUN )
                if TagName in [self.STATUS_SAC_STATUS , self.STATUS_WS_SERVICE] and Value != '1':
                    retrcode = CRITICAL
                    retrcodetag = CRITICAL

                #STATUS_LAST_UPDATE (LAST UPDATE > ACTUAL TIME -1 MINUTE)
                if TagName in [self.STATUS_LAST_UPDATE] and Value !='0.0000':      
                    last_update_time = arrow.get(Value , 'DD/MM/YYYY HH:mm:ss')
                    actual = actual_time.shift(hours=-3, minutes=-5)                    
                    if not last_update_time > actual:
                        retrcode = CRITICAL
                        retrcodetag = CRITICAL

                #STATUS_SAC_OVERRUNS (Value < 10)          
                if TagName in [self.STATUS_SAC_OVERRUNS]:              
                    if Value > '10':                        
                        retrcode = CRITICAL
                        retrcodetag = CRITICAL          
                #STATUS_SAC_CYCLES_SEC (Values = 20)
                if TagName in [self.STATUS_SAC_CYCLES_SEC]:
                    if Value != '20':                        
                        retrcode = CRITICAL
                        retrcodetag = CRITICAL   

            
            if retrcodetag != 0:
                msgerror += 'ERROR: Tagname: {} \n'.format(TagName)

        msgerror += msgdata
 
        return retrcode, msgerror
