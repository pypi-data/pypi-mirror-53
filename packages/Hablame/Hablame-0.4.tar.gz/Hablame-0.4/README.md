# HABLAME CONNECT

Librería de integración de servicio de mensajeria 
[Hablame](https://hablame.co) con django. 

#### Instalación:

> $ pip install Hablame

ó

> $ pipenv install Hablame

Añadir la linea

> 'Hablame' 
 
settings.py en las installed_apps proyecto de django

#### USO

##### Constructor(
    client string,
    api string
)

##### Methods

- Send_SMS(
    
        receiver number,
        message string,
        propagation_date datetime (Opcional)
        reference string (Opcional)
    )
    
    en caso de que propagation_date no se pase por parametro el mensaje se enviara de manera inmediata.
    

**Ejemplo**

>from SY_Hablame from Hablame
>
>instance = Hablame("client_key", "api_Key")
>response = instanse.Send_SMS("Receiver_number", "Message")
>
>print(response)

**Respuesta**

>{
>    "cliente": "10012336",
>    "lote_id": 0,
>    "fecha_recepcion": "2019-10-10 11:06:41",
>    "resultado": 0,
>    "resultado_t": null,
>    "sms_procesados": 1,
>    "referencia": null,
>    "ip": "190.7.130.162",
>    "sms": {
>        "1": {
>            "id": "1570723601789199",
>            "numero": "573116400205",
>            "sms": "hola",
>            "fecha_envio": "2019-10-10 11:06:41",
>            "ind_area_nom": "Colombia Celular",
>            "precio_sms": "6.00000",
>            "resultado_t": "",
>            "resultado": "0"
>        }
>    }
>}

