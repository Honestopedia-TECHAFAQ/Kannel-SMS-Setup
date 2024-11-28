import streamlit as st
from smpplib.client import Client
from smpplib.gsm import make_parts
from smpplib import consts
import logging

logging.basicConfig(filename='sms_sending.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_sms_smpp(host, port, system_id, password, source_addr, destination_addr, message):
    """
    Sends an SMS message via SMPP protocol.
    
    Parameters:
    - host: Kannel SMPP host
    - port: Kannel SMPP port
    - system_id: SMPP system ID
    - password: SMPP password
    - source_addr: Sender address
    - destination_addr: Recipient address
    - message: Text message content
    """
    try:
        client = Client(host, port)
        client.connect()
        client.bind_transmitter(system_id=system_id, password=password)
        parts, encoding_flag, msg_type_flag = make_parts(message)
        for part in parts:
            client.send_message({
                'source_addr_ton': consts.SMPP_TON_ALNUM,
                'source_addr': source_addr,
                'dest_addr_ton': consts.SMPP_TON_INTERNATIONAL,
                'destination_addr': destination_addr,
                'short_message': part,
                'data_coding': encoding_flag,
                'esm_class': msg_type_flag,
            })
        
        logging.info(f"SMS sent successfully to {destination_addr} via SMPP.")
        st.success("Message sent successfully.")

        client.unbind()
        client.disconnect()
    except Exception as e:
        logging.error(f"Failed to send SMS to {destination_addr} via SMPP: {e}")
        st.error(f"Error occurred: {e}")
st.title("SMPP SMS Sending Tool")
st.subheader("Enter SMPP Connection Details and SMS Content")

smpp_host = st.text_input("SMPP Host", "your-kannel-server")  
smpp_port = st.number_input("SMPP Port", min_value=1, value=2775)  
system_id = st.text_input("SMPP System ID", "your_smpp_system_id")  
password = st.text_input("SMPP Password", "your_smpp_password", type="password")  
source_addr = st.text_input("Source Address", "SenderID")  
destination_addr = st.text_input("Destination Address (Recipient Number)", "recipient_number") 
message = st.text_area("Message", "Hello, this is a test message via SMPP!")  
if st.button("Send SMS"):
    if smpp_host and system_id and password and destination_addr and message:
        send_sms_smpp(smpp_host, smpp_port, system_id, password, source_addr, destination_addr, message)
    else:
        st.error("Please fill in all the required fields.")
