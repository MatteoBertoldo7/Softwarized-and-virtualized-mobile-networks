from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet
import logging
import time

class SDNController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SDNController, self).__init__(*args, **kwargs)
        self.byte_trasmessi = {}  # Dizionario per tenere traccia dei byte trasmessi per ciascuno switch
        self.byte_ricevuti = {}   # Dizionario per tenere traccia dei byte ricevuti per ciascuno switch
        self.soglia_di_allarme = 1000000  # Soglia di allarme in byte (ad esempio, 1 MB)
        
    #PROVO A METTERE CHE SE IL WIFI PUBBLICO SUPERA 90%, ALTRE AREE CONDIVIDONO
    #LA PROPRIA RETE (TRANNE SECURITY)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def flow_stats_reply_handler(self, ev):
        # Gestisci le statistiche di flusso ricevute da uno switch
        current_time = time.time()  # Ottieni il tempo corrente
        elapsed_time = current_time - self.last_measurement_time  # Calcola l'intervallo di tempo trascorso
        self.last_measurement_time = current_time  # Aggiorna il tempo dell'ultima misurazione
        msg = ev.msg
        dp_id = msg.datapath.id

        for stat in msg.body:
            byte_trasmessi = stat.byte_count  # Byte trasmessi nel flusso
            byte_ricevuti = stat.packet_count * 1024  # Byte ricevuti nel flusso (moltiplicati per 1024 per convertirli in byte)

            # Aggiorna le variabili di utilizzo della banda per lo switch
            self.byte_trasmessi[dp_id] = byte_trasmessi
            self.byte_ricevuti[dp_id] = byte_ricevuti

            # Controlla se l'utilizzo della banda supera la soglia di allarme
            utilizzo_banda = (byte_trasmessi + byte_ricevuti) / elapsed_time
            if utilizzo_banda > self.soglia_di_allarme:
                logging.warning("L'utilizzo della banda per lo switch %s ha superato la soglia di allarme.", dp_id)
                self.condividi_banda(dp_id)

    def condividi_banda(self, switch_id):
# Implementa la logica per la condivisione dinamica della banda
    
    # Esempio: se il WiFi pubblico supera il 90% dell'utilizzo della banda
    # e il switch specifico supera la soglia di allarme, ridistribuisci la banda
    
    if switch_id == 'switch_wifi_pubblico':
        wifi_pubblico_utilizzo = self.byte_trasmessi.get(switch_id, 0) + self.byte_ricevuti.get(switch_id, 0)
        if wifi_pubblico_utilizzo > 0.9 * self.soglia_di_allarme:
            # Ridistribuisci la banda tra altre aree di rete, ad eccezione della sicurezza
            self.redistribuisci_banda(wifi_pubblico_utilizzo)
    
    # Altre logiche di condivisione della banda in base ai tuoi requisiti

    def redistribuisci_banda(self, utilizzo_wifi_pubblico):
    # Esempio di ridistribuzione della banda tra le altre aree di rete
    # In questa implementazione fittizia, si assume che ci siano 4 aree di rete
    # e la banda venga suddivisa equamente tra di loro
    num_aree_di_rete = 4
    banda_per_area = utilizzo_wifi_pubblico / num_aree_di_rete
    
    for switch_id in self.byte_trasmessi:
        if switch_id != 'switch_wifi_pubblico' and switch_id != 'switch_sicurezza':
            self.byte_trasmessi[switch_id] = banda_per_area
            self.byte_ricevuti[switch_id] = banda_per_area

    # Puoi implementare ulteriori logiche di ridistribuzione della banda in base alle tue esigenze
    

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        pkt = packet.Packet(msg.data)
    
        # Analizza il pacchetto Ethernet (SWITCH SDN LAVORANO A LIVELLO ETHERNET)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
    
        if eth_pkt:
            # Estrai gli indirizzi MAC di origine e destinazione dal pacchetto Ethernet
            src_mac = eth_pkt.src
            dst_mac = eth_pkt.dst
            
            # Puoi calcolare l'utilizzo della banda in base ai pacchetti ricevuti/trasferiti
            # Ad esempio, tieni traccia dei byte totali trasmessi e ricevuti
            # Controlla l'utilizzo della banda per uno switch specifico
            dp_ip = msg.datapath.id
            byte_trasmessi = self.byte_trasmessi.get(dp_ip, 0)
            byte_ricevuti = self.byte_ricevuti.get(dp_ip, 0)
            
            # Calcola l'utilizzo della banda in base al numero di byte trasmessi e ricevuti
            utilizzo_banda = (byte_trasmessi + byte_ricevuti) / (elapsed_time)  # Calcola l'utilizzo in byte al secondo
                        
            if utilizzo_banda > self.soglia_di_allarme:
                logging.warning("L'utilizzo della banda ha superato la soglia di allarme.")
                
                # Puoi intraprendere azioni specifiche qui in caso di superamento della soglia
                # Ad esempio, invia una notifica, registra l'evento, ecc.
                # Inoltre, è possibile definire ulteriori azioni da intraprendere in questa condizione
    
    # ...

if __name__ == '__main__':
    from ryu.cmd import manager
    manager.main(['ryu', 'simple_switch_13.py'])
