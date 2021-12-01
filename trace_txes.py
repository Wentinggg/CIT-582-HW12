from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
from datetime import datetime

rpc_user = 'quaker_quorum'
rpc_password = 'franklin_fought_for_continental_cash'
rpc_ip = '3.134.159.30'
rpc_port = '8332'

rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (rpc_user, rpc_password, rpc_ip, rpc_port))


###################################

class TXO:
    def __init__(self, tx_hash, n, amount, owner, time):
        self.tx_hash = tx_hash  # (string) the tx_hash on the Bitcoin blockchain
        self.n = n  # (int) the position of this output in the transaction
        self.amount = amount  # (int) the value of this transaction output (in Satoshi),
        # Make sure that you store “amount” as integer, not a floating point number
        self.owner = owner  # (string) the Bitcoin address of the owner of this output
        self.time = time  # (Datetime) the time of this transaction as a datetime object
        self.inputs = []  # (TXO[]) a list of TXO objects

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.tx_hash) + "\n"
        for tx in self.inputs:
            ret += tx.__str__(level + 1)
        return ret

    def to_json(self):
        fields = ['tx_hash', 'n', 'amount', 'owner']
        json_dict = {field: self.__dict__[field] for field in fields}
        json_dict.update({'time': datetime.timestamp(self.time)})
        if len(self.inputs) > 0:
            for txo in self.inputs:
                json_dict.update({'inputs': json.loads(txo.to_json())})
        return json.dumps(json_dict, sort_keys=True, indent=4)

    @classmethod
    def from_tx_hash(cls, tx_hash, n=0):
        # YOUR CODE HERE
        tx = rpc_connection.getrawtransaction(tx_hash, True)
        time = datetime.fromtimestamp(tx['time'])
        amount = int(tx['vout']['value'])
        owner = tx['vout']['addresses']['address']

        return cls(tx_hash, n, amount, owner, time)

    def get_inputs(self, d=1):
        # YOUR CODE HERE
        self.get_inputs(self.inputs[d], d)
        if d > 1:
            d -= 1
            self.get_inputs(self.inputs[d], d)
