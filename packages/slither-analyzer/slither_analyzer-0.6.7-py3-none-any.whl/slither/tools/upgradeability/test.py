import logging
from slither import Slither
from slither.tools.upgradeability.compare_variables_order import compare_variables_order_proxy
from slither.tools.upgradeability.compare_function_ids import compare_function_ids
from slither.tools.upgradeability.check_initialization import check_initialization

logging.basicConfig()
logging.getLogger("Slither-check-upgradeability").setLevel(logging.INFO)
logging.getLogger("Slither").setLevel(logging.INFO)

slither = Slither('.', truffle_ignore_compile=True)

proxy = slither.get_contract_from_name('Proxy')
proxy_targets = [c.name for c in slither.contracts if proxy in c.inheritance]
proxy_targets = [c[:-len('Proxy')] for c in proxy_targets]

check_initialization(slither)

for target in proxy_targets:
    print('######################')
    print(f'Check {target}')

    compare_function_ids(slither, target, slither, proxy.name)

    compare_variables_order_proxy(slither, target, slither, proxy.name)


from manticore.ethereum import Plugin

class Tracer(Plugin):
    '''
        Manticore plugin that detects if there was a store in the memory
        Store in context['Deepstate']['did_write_in_memory'] the result
        context['Deepstate'] must be init prior running the plugin
    '''

    def did_close_transaction_callback(self, state, tx):
        self.manticore.m.generate_testcase(state, "Report")


m.register_plugin(Tracer())


m.transaction(caller=your_user,
              address=your_contract,
              value=m.make_symbolic_value(),
              data=m.make_symbolic_buffer(320))
