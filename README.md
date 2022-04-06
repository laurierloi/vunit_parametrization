# Vunit Parametrization

Sample code to parametrize VUnit tests.

Objective is mainly to show how I used parametrization and to discover methods in which it could be expanded.

At the moment, Parametrization is used to:
  - Create various configurations of the test system (frequencies, width, enable/disabled components)
  - Support multiple entities with the same test bench (axi-module or register-mapped module)

Ideally it would support:
  - Pytest Fixtures to create higher level configuration of the test
    - have multiple cheby configurations for example
    - parametrization could be handled through fixtures?
  - Ability to expect tests to fail with a given parameter set - seem to match: https://github.com/VUnit/vunit/issues/293
	- (Actual PASS) Assert check for invalid parameters
	- (Actual SKIP) Yet-unsupported parameter combination which will fail tests expectedly

What should be integrated in VHDL instead of python:
  - VHDL fixtures: the selection by generate of which entity/architecture to test
  - Bad Stimulus: the core handles incorrect inputs appropriatly, it should be a PASS in my tests
