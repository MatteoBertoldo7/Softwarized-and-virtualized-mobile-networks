from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet
import logging

class SDNController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SDNController, self).__init__(*args, **kwargs)
        self.byte_trasmessi = {}  # Dizionario per tenere traccia dei byte trasmessi per ciascuno switch
        self.byte_ricevuti = {}   # Dizionario per tenere traccia dei byte ricevuti per ciascuno switch
        self.soglia_di_allarme = 1000000  # Soglia di allarme in byte (ad esempio, 1 MB)
        
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Definisci le regole di flusso per ciascuna slice
        # Ad esempio, regole per la slice WiFi pubblico
        if datapath.id == 1:  # Supponiamo che lo switch per WiFi pubblico abbia datapath ID 1
            match = parser.OFPMatch(eth_type=0x0800, ip_proto=6, tcp_dst=80)
            actions = [parser.OFPActionOutput(ofproto.OFPP_NORMAL)]
            self.add_flow(datapath, 100, match, actions)



    #PROVO A METTERE CHE SE IL WIFI PUBBLICO SUPERA 90%, ALTRE AREE CONDIVIDONO
    #LA PROPRIA RETE (TRANNE SECURITY)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def flow_stats_reply_handler(self, ev):
        # Gestisci le statistiche di flusso ricevute da uno switch
        msg = ev.msg
        dp_id = msg.datapath.id

        for stat in msg.body:
            byte_trasmessi = stat.byte_count  # Byte trasmessi nel flusso
            byte_ricevuti = stat.packet_count * 1024  # Byte ricevuti nel flusso (moltiplicati per 1024 per convertirli in byte)

            # Aggiorna le variabili di utilizzo della banda per lo switch
            self.byte_trasmessi[dp_id] = byte_trasmessi
            self.byte_ricevuti[dp_id] = byte_ricevuti

            # Controlla se l'utilizzo della banda supera la soglia di allarme
            utilizzo_banda = byte_trasmessi + byte_ricevuti
            if utilizzo_banda > self.soglia_di_allarme:
                logging.warning("L'utilizzo della banda per lo switch %s ha superato la soglia di allarme.", dp_id)
                self.condividi_banda(dp_id)

        def condividi_banda(self, switch_id):
        # Implementa la logica per la condivisione dinamica della banda
        # Puoi attivare la condivisione della banda tra le diverse aree di rete qui
        # Ad esempio, regola le politiche di instradamento in base alle esigenze
        pass

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
            byte_trasmessi = self.byte_trasmessi.get(dp_id, 0)
            byte_ricevuti = self.byte_ricevuti.get(dp_id, 0)
            
            # Calcola l'utilizzo della banda in base al numero di byte trasmessi e ricevuti
            utilizzo_banda = (byte_trasmessi + byte_ricevuti) / (tempo_trascorso_in_secondi)  # Calcola l'utilizzo in byte al secondo
                        
            if utilizzo_banda > soglia_di_allarme:
                logging.warning("L'utilizzo della banda ha superato la soglia di allarme.")
                
                # Puoi intraprendere azioni specifiche qui in caso di superamento della soglia
                # Ad esempio, invia una notifica, registra l'evento, ecc.
                # Inoltre, è possibile definire ulteriori azioni da intraprendere in questa condizione.
    
    # ...



    

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match,
            instructions=inst, idle_timeout=0, hard_timeout=0,
            buffer_id=ofproto.OFP_NO_BUFFER, out_port=ofproto.OFPP_ANY,
            out_group=ofproto.OFPG_ANY, flags=0
        )
        datapath.send_msg(mod)

    # Aggiungi altre funzioni e logica per la gestione delle slice, la condivisione di banda, ecc.

if __name__ == '__main__':
    from ryu.cmd import manager
    manager.main(['ryu', 'simple_switch_13.py'])
