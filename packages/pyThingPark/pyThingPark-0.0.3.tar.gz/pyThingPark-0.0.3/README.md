# pyThingPark

Python implementation of LoRaWAN standard and ThingPark Wireless tunnel API

## Installation
PyThingPark doesn't support Python2 in order to keep maintenance to the minimum. 
To install Python3, refer to [https://www.python.org/downloads](https://www.python.org/downloads/)

To implement LoRaWAN MIC calculation and encryption, pyThingPark make use of Python standard cryptographic library `cryptography`.

pyThingPark is packaged and distributed on pip
```
pip3 install pyThingPark
```

To compile a .whl built distribution file + tar.gz source, and upload on PyPi, please refer to [Python Package instructions](https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives)

## Functionalities
This package is implemented as a library and contains no executable file. This is meant to help the analysis of LoRaWAN messages as well as the implementation of Application Server integrating with ThingPark Wireless via the tunnel interface.

### lorawan.py: Python loRaWAN implementation
***lorawan.py*** implements all LoRaWAN message types: JoinRequest, JoinAccept, UlUnconfFrame, DlUnconfFrame, UlConfFrame, DlConfFrame as objects.

Messages can be create with the `__init__` method by providing all sub-fields, or by importing directly the Physical Payload displayed in Actility LRC logs.
For example,

    17:33:32.472 [DET] (lrc-lora-0)    [LoRa.c:927] LoRaMAC_UpLink '0001000171ac293df0bd2d6e6645d32301e2e2f98f810f'
    17:33:32.472 [DET] (lrc-lora-0)    [join.c:3651] Join Request AppEUI: 90dffb0000000000 DevEUI:90dffbbd5813c019 DevNonce:2d2c
can be imported as a JoinRequest message for analysis with the following command:

    >>> from lorawan import JoinRequest
    >>> jr = JoinRequest.fromPayload("0001000171ac293df0bd2d6e6645d32301e2e2f98f810f")
    >>> jr
    {'MessageType': 'JoinReq', 'MACVersion': '1.0', 'PHYPayload': '0001000171ac293df0bd2d6e6645d32301e2e2f98f810f', 'JoinEUI': 'f03d29ac71010001', 'DevEUI': '0123d345666e2dbd', 'DevNonce': 'e2e2', 'MIC': 'f98f810f'}
and MIC can be verified by providing AppKey as an input:

    >>> jr.computeMIC(AppKey="28125FFD247F3D933834B4A2862CE05D")
    'f98f810f'
JoinAccept is automatically decrypted if provided in encrypted form via `fromPayload` method (and AppKey is mandatory in this case)

    >>> from lorawan import JoinAccept
    >>> JoinAccept.fromPayload("2051b239de5da07db5a8844c4714488cf116815975a04e70bf86282ed11eaa5289", "28125FFD247F3D933834B4A2862CE05D")
    {'MessageType': 'JoinAns', 'MACVersion': '1.0', 'PHYPayload': '20096095020000d07e94052301184f84e85684b85e84886684586e8400a782a999', 'JoinNonce': '956009', 'NetId': '000002', 'DevAddr': '05947ed0', 'DLSettings': '23', 'RxDelay': '01', 'CFList': '00846e58846688845eb88456e8844f18', 'MIC': 'a782a999'}

### device.py: Python LoRaWAN key derivation implementation
***device.py*** implements LW1.0 key derivation functions, making it simple to check session keys are computed correctly on the device after receiving the JoinAccept.

Example code:

    >>> d = Device("FFFFFFAA00AC7000","FFFFFFBB00000000","037407b0a2eb121d99b2ad03b605af3a",None,None)
    >>> jr = lorawan.JoinRequest.fromPayload("0x0000000000bbffffff0070ac00aaffffffc3f5d6de8f3e")
    >>> ja = lorawan.JoinAccept.fromPayload("202573C61502E510C4802CEE5C076A6D9C1329A8F89689BA77BFE13F5A7CD15809",d.AppKey)
    >>> print(d.deriveKeys(ja.JoinNonce, ja.NetId, jr.DevNonce))
    ('6f10ae090fd5f6ecf0a8e37638abb2da', 'a172e9f886f3835f3f7ebaa51a658b19')
    
### uplinkTunnel.py: Python ThingParkWireless tunnel implementation
This part of the library aims at providing a reference to integrate AS with TP Wireless with security options enabled.

`DevEUI_uplink`decodes TPW document as XML or JSON form, and provide ability to decrypt payload in case it is sent encrypted by TPW (SSM or HSM mode):

    >>> uplink = DevEUI_uplink("<?xml version='1.0' encoding='UTF-8'?><DevEUI_uplink xmlns='http://uri.actility.com/lora'><Time>2019-08-05T17:33:51.362+02:00</Time><DevEUI>0123D345666E2DBD</DevEUI><FPort>1</FPort><FCntUp>1</FCntUp><MType>2</MType><FCntDn>1</FCntDn><payload_hex>afac18845bbe3771708042</payload_hex><mic_hex>dcdcc1f5</mic_hex><Lrcid>00000127</Lrcid><LrrRSSI>-65.000000</LrrRSSI><LrrSNR>12.500000</LrrSNR><SpFact>9</SpFact><SubBand>G1</SubBand><Channel>LC3</Channel><DevLrrCnt>1</DevLrrCnt><Lrrid>C000146F</Lrrid><Late>0</Late><LrrLAT>43.640781</LrrLAT><LrrLON>7.017418</LrrLON><Lrrs><Lrr><Lrrid>C000146F</Lrrid><Chain>0</Chain><LrrRSSI>-65.000000</LrrRSSI><LrrSNR>12.500000</LrrSNR><LrrESP>-65.237602</LrrESP></Lrr></Lrrs><CustomerID>100118249</CustomerID><CustomerData>{'alr':{'pro':'LORA/Generic','ver':'1'}}</CustomerData><ModelCfg>0</ModelCfg><AppSKey>439d42627c5afe3d4d536340646621a2</AppSKey><BatteryLevel>0</BatteryLevel><BatteryTime>2019-08-05T17:33:51.362+02:00</BatteryTime><Margin>7</Margin><InstantPER>0.000000</InstantPER><MeanPER>0.000000</MeanPER><DevAddr>05947ED0</DevAddr><AckRequested>0</AckRequested><rawMacCommands>060007</rawMacCommands><TxPower>16.000000</TxPower><NbTrans>1</NbTrans></DevEUI_uplink>")
    >>> ASTK = "dbfb0939c448ff1fbf84e84d6ac8ce98"
    >>> uplink.decryptPayload(ASTK)

`UplinkTunnel`  take HTTP query params as an extra input, and can compute or verify the UL security token (taking Transport Interface Application Key TIAK as input)

    >>> query_params = 'AS_ID=sink&LrnFPort=1&Time=2019-04-29T18:21:17.290+02:00&Token=d306f33c239a9c45d160e0cd6e4071e22a4f4b426f892a0651cf622e81369f3d&LrnDevEui=0024AEB3C02BE1C4&LrnInfos=TWA_100122002.8962.AS-1-4458785'
    >>> TIAK = 'bec499c69e9c939e413b663961636c61'
    >>> tunnel = UplinkTunnel(uplink, query_params,TIAK)
    >>> expectedToken = tunnel.token()

### dxMaker.py: Python DX maker wrapper
***dxMaker.py*** is a Python wrapper using [DX API](https://dx-api.thingpark.com/maker/latest/api/).
It can be used to simply provision devices in ThingPark Activation on TP labs instance.

In order to use DX, you must first get a bearer token for authentication.
This can be done using `DxAdmin` class with necessary credentials:

    >>> dx = DxAdmin("my-account@acme.fr", "a_clever_password", platform="js-labs-api")
    >>> bearerToken = dx.getBearerToken()

Once a bearer token is available (it can of course also be generated directly on [DX Admin](https://dx-api.thingpark.com/admin/latest/swagger-ui/index.html?shortUrl=tpdx-admin-api-contract.json)), you can use it to create a `DxMaker`instance and create FactoryDevice on TP Labs via DX:

    >>> bearerToken = "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6WyJTVUJTQ1JJQkVSOjEwMDAwMDA4NSJdLCJleHAiOjE1Njk4MzM4NTMsImp0aSI6ImM4ZGI4Y2RmLTcxNGYtNGE3OS1hNGZiLTI0OWYxNWVhMGIxYiIsImNsaWV94FDpZCI6ImpzLWxhYnMtYXBpL3JhcGhhZWwuYXBmZWxkb3JmZXItanMtbGFicy1zdWJAYWN0aWxpdHkuY29tIn0.KQaDUlrp6lcPJU9Gz5Re25WlHzMvIW75aef1oECCBGMOcIw9u_I7SyyZOMp1K9-AuJOY60DyfXLnVMIm_3CWaw"
    >>> dx = dxMaker.DxMaker(bearerToken)
    >>> device = dxMaker.FactoryDevice(DevEUI=my.devEUI, JoinEUI=my.joinEUI, TkmInfo=my.tkmInfo)
    >>> dx.postFactoryDevice(device)
    >>> dx.deleteFactoryDevice(device.deviceJson["deviceEUI"])

A simple `FactoryDevice` class is provided to store device information necessary for the Join Server, and only Microchip ECC608 provisioning is supported for now. Only pre-commissioning of the Join Server is supported in this version, so no ASTK handling is implemented in the wrapper.
  
## Extending the package
Future development may include
* Complete implementation of remaining LoRaWAN messages
* Decoding of MAC commands
* LoRaWAN1.0.4 / Class B
* LoRaWAN1.1
* Downlink messages

This package is implemented as a library, Each function implementation is validated in the `main` part as a set of `assert` so we can easily test non-regressions.