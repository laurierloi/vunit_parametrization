# ParametrizeTest does a product of a dict of parameter lists
# It does not support more fine-grained combination of parameter like one could
#  in pytest by having multiple `parametrize` decorators
class ParametrizeTest():
    def __init__(self, params):
        self.params = params

    @staticmethod
    def encode(config):
        return ", ".join(["%s:%s" % (key, str(config[key])) for key in config])

    @property
    def combined_dicts(self):
        key_order = []
        params_list = []
        for key, param in self.params.items():
            key_order.append(key)
            params_list.append(param)

        combined_dicts = []
        for t in product(*params_list, repeat=1):
            d = {key: t[i] for i, key in enumerate(key_order)}
            combined_dicts.append(d)
        return combined_dicts

# Add tests to the testbench using the parameter dict
#  it could probably be replaced by a python fixture, but I'm not clear on the
#  way to do so at this point.
def add_sync_tests(util, params, tb="sync_tb"):
    tb_sync = util.add_test_bench(tb)
    parametrize = ParametrizeTest(params)
    sync_combination = parametrize.combined_dicts

    for i, q in enumerate(sync_combination):
        tb_sync.add_config(
            f'Sync Parametrized Test {i:03}: {q["interface"]}, {q["period_clk_req_ps"]:04}, {q["period_clk_ack_ps"]:04}, {q["phase_clk_req_to_clk_ack_ps"]:+04}',
            generics=dict(encoded_tb_config=parametrize.encode(q)),
        )

if __name__ == '__main__':
    # Util is a wrapper to manage package/libraries/simulator configuration and run vunit
    util = VUnitUtil()

    sync_params = {
        # interface defines which architecture to instantiate
        # It acts as a VHDL fixture
        # I use https://gitlab.cern.ch/cohtdrivers/cheby to generate the core's bus interfaces
        # I generally create a `sync_base.vhdl` entity which has a register-map interface
        # Then I create a `sync.vhdl` wrapper entity which has an axi interface
        # I test the base module and the axi module using the same suite
        'interface': ['reg', 'axi'],
        'period_clk_req_ps': [1000, 4000],
        'period_clk_ack_ps': [1000, 8000],
        'phase_clk_req_to_clk_ack_ps': [0, -500, 100],
    }

    add_sync_tests(util, sync_params)

    # Some cases where I would like to catch a falling test in run
    #  - I intently provided a bad configuration for the core generic's to validate that the internal
    #    asserts will not let it pass
    #  - A parameter combination is not yet supported by my system and is expected to fail
    #    At the moment, I would filter-out the condition manually in `add_sync_tests` to skip
    util.run()

