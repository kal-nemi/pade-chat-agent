from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.acl.messages import ACLMessage


class ChatAgent(Agent):
    def __init__(self, aid, receiver_agent):
        super().__init__(aid)
        self.receiver_agent = receiver_agent

    def react(self, message):
        super().react(message)
        display_message(self.aid.localname, 'Message received from {}'.format(message.sender.name))
        display_message(self.aid.localname, 'Message is {}'.format(message.content))
        self.send_message()

    def on_start(self):
        super().on_start()
        display_message(self.aid.localname, 'Chat agent start...')
        self.send_message()

    def send_message(self):
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(self.receiver_agent)
        self.add_all_agents(message.receivers)
        msg = input("Enter message: ")
        message.set_content(msg)
        self.send(message)

    def add_all_agents(self, receivers):
        for receiver in receivers:
            self.agentInstance.table[receiver.localname] = receiver

if __name__ == '__main__':
    agents = list()
    receiver_aid = AID(name='agent2@localhost:{}'.format(30001))
    # receiverAgent = ReceiverAgent(receiver_agent_aid)
    # agents.append(receiverAgent)
    chat_agent = ChatAgent(AID(name='agent1@localhost:{}'.format(30000)), receiver_aid)
    agents.append(chat_agent)

    start_loop(agents)
