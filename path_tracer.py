from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()
mac_to_port = {}

def _handle_ConnectionUp(event):
    log.info("Switch %s connected", event.dpid)

def _handle_PacketIn(event):
    packet = event.parsed
    dpid = event.dpid
    in_port = event.port

    if not packet.parsed:
        return

    src = packet.src
    dst = packet.dst

    mac_to_port.setdefault(dpid, {})
    mac_to_port[dpid][src] = in_port

    if dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][dst]
    else:
        out_port = of.OFPP_FLOOD

    # PATH TRACE
    log.info("[PATH] Switch %s: %s → %s via port %s",
             dpid, src, dst, out_port)

    # Install flow rule
    msg = of.ofp_flow_mod()
    msg.match.dl_dst = dst
    msg.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg)

    # Send packet
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=out_port))
    msg.in_port = in_port
    event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Path Tracing Controller Started")