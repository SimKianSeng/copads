import sys
import os
import copy
import pprint
import unittest

sys.path.append(os.path.join(os.path.dirname(os.getcwd()), 'copads'))
import neural as n

brainfile = 'testbrain.db'

class testSimpleBrain(unittest.TestCase):
    '''
    setUp(self): add_neuron()
    setUp(self): add_synapse(x[0], x[1])

    testAddNeuron1(self): get_neurons('alive')
    testAddNeuron1(self): add_neuron()

    testAddNeuron2(self): add_neuron(name='test', summation='sumtest', transfer='transfer_test', threshold='0.1', pstate='0.11')
    testAddNeuron2(self): get_neuronID_from_name('test')
    testAddNeuron2(self): get_name_from_neuronID(nID)
    testAddNeuron2(self): get_neuron_state(nID, 'summation')
    testAddNeuron2(self): get_neuron_state(nID, 'pstate')
    
    testGetSynapse(self): get_synapses('1', 'weight')
    testGetSynapse(self): get_synapses('1', 'all')
    testGetSynapse(self): get_synapses('2', 'weight')

    testAddSynapse1(self): add_synapse('1', '8')

    testDeleteNeuron(self): get_neurons('alive')
    testDeleteNeuron(self): get_synapses('3', 'weight')
    testDeleteNeuron(self): get_synapses('6', 'weight')
    testDeleteNeuron(self): delete_neuron('6')
    testDeleteNeuron(self): get_neurons('alive')
    testDeleteNeuron(self): get_synapses('3', 'weight')
    testDeleteNeuron(self): get_synapses('6', 'weight')

    testDeleteOrphanedNeurons(self): delete_orphaned_neurons()

    testDeleteSynapse(self): get_synapses('1', 'weight')
    testDeleteSynapse(self): delete_synapse('1', '3')
    testDeleteSynapse(self): get_synapses('1', 'weight')

    testDeleteSynapseByState(self): add_synapse(x[0], x[1])
    testDeleteSynapseByState(self): get_all_synaptic_states('weight')
    testDeleteSynapseByState(self): delete_synapse_by_state(0.1, 'lowest', 'weight')
    testDeleteSynapseByState(self): get_all_synaptic_states('weight')

    testSetNeuronState(self): set_neuron_state('1', 'trialstate', 0.5)
    testSetNeuronState(self): get_neuron_state('1', 'trialstate')

    testSetSynapseState(self): set_synapse_state('1', '2', 'testvalue', 'teststate')
    testSetSynapseState(self): get_synapse_state('1', '2', 'teststate')

    testAddInputChannel(self): get_input_values('1')
    testAddInputChannel(self): add_input_channel('eye', '1')
    testAddInputChannel(self): get_input_values('1')

    testSetInput(self): set_input('eye', {'1': 0.9})
    testSetInput(self): get_input_values('1')
    testSetInput(self): set_input('eye', {'1': 0.7})
    testSetInput(self): get_input_values('1')
    testSetInput(self): set_input('eye', {'1': 0.15})
    testSetInput(self): get_input_values('1')

    testExecuteNeuron1(self): set_input('eye', {'1': 0.15})
    testExecuteNeuron1(self): get_input_values('1')
    testExecuteNeuron1(self): get_neuron_state('1', 'pstate')
    testExecuteNeuron1(self): get_input_values('2')
    testExecuteNeuron1(self): get_input_values('3')
    testExecuteNeuron1(self): execute_neuron('1', 'pstate', 'weight')
    testExecuteNeuron1(self): get_neuron_state('1', 'pstate')
    testExecuteNeuron1(self): get_input_values('2')
    testExecuteNeuron1(self): get_input_values('3')

    testExecuteNeuron2(self): set_input('eye', {'1': 0.15})
    testExecuteNeuron2(self): get_input_values('1')
    testExecuteNeuron2(self): get_neuron_state(str(ID), state='pstate') 
    testExecuteNeuron2(self): execute_neuron(str(ID), 'pstate', 'weight')
    testExecuteNeuron2(self): get_neuron_state(str(ID), state='pstate')
    '''
    def setUp(self):
        self.brain = n.brain(brainfile)
        self.brain.format()
        for i in range(10):
            self.brain.add_neuron()
        for x in [('1', '2'), ('1', '3'), ('2', '4'), ('4', '5'), ('3', '6'),
                  ('5', '7'), ('6', '7')]:
            self.brain.add_synapse(x[0], x[1])

    def testAddNeuron1(self):
        nIDs = self.brain.get_neurons('alive')
        self.assertEqual(len(nIDs), 10)
        for i in range(5):
            self.brain.add_neuron()
        nIDs = self.brain.get_neurons('alive')
        self.assertEqual(len(nIDs), 15)

    def testAddNeuron2(self):
        nID = self.brain.add_neuron(name='test', summation='sumtest',
                                    transfer='transfer_test', threshold='0.1',
                                    pstate='0.11')
        ID = self.brain.get_neuronID_from_name('test')
        self.assertEqual(nID, ID)
        name = self.brain.get_name_from_neuronID(nID)
        self.assertEqual(name, 'test')
        summation = self.brain.get_neuron_state(nID, 'summation')
        self.assertEqual(summation, 'sumtest')
        pstate = self.brain.get_neuron_state(nID, 'pstate')
        self.assertEqual(pstate, '0.11')

    def testGetSynapse(self):
        nIDs = self.brain.get_synapses('1', 'weight')
        self.assertEqual(nIDs, ['2', '3'])
        nIDs = self.brain.get_synapses('1', 'all')
        self.assertEqual(nIDs, ['2', '3'])
        nIDs = self.brain.get_synapses('2', 'weight')
        self.assertEqual(nIDs, ['4'])

    def testAddSynapse1(self):
        self.brain.add_synapse('1', '8')
        nIDs = self.brain.get_synapses('1', 'weight')
        self.assertEqual(nIDs, ['2', '3', '8'])

    def testDeleteNeuron(self):
        # before deleting neuron #6 - 10 neurons present
        nIDs = self.brain.get_neurons('alive')
        self.assertEqual(len(nIDs), 10)
        # before deleting neuron #6 - (#3 --> #6)
        nIDs = self.brain.get_synapses('3', 'weight')
        self.assertEqual(nIDs, ['6'])
        # before deleting neuron #6 - (#6 --> #7)
        nIDs = self.brain.get_synapses('6', 'weight')
        self.assertEqual(nIDs, ['7'])
        # delete neuron #6
        self.brain.delete_neuron('6')
        # after deleting neuron #6 - 9 neurons present
        nIDs = self.brain.get_neurons('alive')
        self.assertEqual(len(nIDs), 9)
        # after deleting neuron #6 - (#3 --> nothing)
        nIDs = self.brain.get_synapses('3', 'weight')
        self.assertEqual(nIDs, [])
        # after deleting neuron #6 - (nothing --> #7)
        nIDs = self.brain.get_synapses('6', 'weight')
        self.assertEqual(nIDs, [])

    def testDeleteOrphanedNeurons(self):
        self.brain.delete_orphaned_neurons()
        nIDs = self.brain.get_neurons('alive')
        self.assertEqual(len(nIDs), 7)
        self.assertEqual(nIDs, ['1', '2', '3', '4', '5', '6', '7'])

    def testDeleteSynapse(self):
        nIDs = self.brain.get_synapses('1', 'weight')
        self.assertEqual(nIDs, ['2', '3'])
        self.brain.delete_synapse('1', '3')
        nIDs = self.brain.get_synapses('1', 'weight')
        self.assertEqual(nIDs, ['2'])

    def testDeleteSynapseByState(self):
        # add 14 more synapses (only 7 in setUp) to 21
        for x in [('6', '8'), ('6', '9'), ('6', '10'), 
                  ('5', '8'), ('5', '9'), ('5', '10'), 
                  ('7', '10'), ('8', '10'), ('9', '10'),
                  ('3', '8'), ('3', '9'), ('3', '10'), 
                  ('4', '8'), ('4', '9')]:
            self.brain.add_synapse(x[0], x[1])
        # remove lowest 10% of synapses - 2 synapses removed (19 remaining)
        old_synaptic_states = self.brain.get_all_synaptic_states('weight')
        self.brain.delete_synapse_by_state(0.1, 'lowest', 'weight')
        new_synaptic_states = self.brain.get_all_synaptic_states('weight')
        self.assertEqual(len(new_synaptic_states), 19)

    def testSetNeuronState(self):
        self.brain.set_neuron_state('1', 'trialstate', 0.5)
        pstate = self.brain.get_neuron_state('1', 'trialstate')
        self.assertEqual(pstate, '0.5')

    def testSetSynapseState(self):
        self.brain.set_synapse_state('1', '2', 'testvalue', 'teststate')
        value = self.brain.get_synapse_state('1', '2', 'teststate')
        self.assertEqual(value, 'testvalue')

    def testAddInputChannel(self):
        # before adding input channel - there is no input into neuron #1
        input_vector = self.brain.get_input_values('1')
        self.assertEqual(len(input_vector), 0)
        # adding input channel #eye
        self.brain.add_input_channel('eye', '1')
        # after adding input channel - there is 1 input into neuron #1
        input_vector = self.brain.get_input_values('1')
        self.assertEqual(len(input_vector), 1)

    def testSetInput(self):
        # test 1
        self.brain.set_input('eye', {'1': 0.9})
        input_vector = self.brain.get_input_values('1')
        self.assertEqual(input_vector, [0.9])
        # test 2
        self.brain.set_input('eye', {'1': 0.7})
        input_vector = self.brain.get_input_values('1')
        self.assertEqual(input_vector, [0.7])
        # test 3
        self.brain.set_input('eye', {'1': 0.15})
        input_vector = self.brain.get_input_values('1')
        self.assertEqual(input_vector, [0.15])

    def testExecuteNeuron1(self):
        # set an input into neuron #1
        self.brain.set_input('eye', {'1': 0.15})
        input_vector = self.brain.get_input_values('1')
        self.assertEqual(input_vector, [0.15])
        # get data before execution of neuron #1
        old_pstate = self.brain.get_neuron_state('1', 'pstate')
        old_input2 = self.brain.get_input_values('2')
        old_input3 = self.brain.get_input_values('3')
        # execute neuron #1
        self.brain.execute_neuron('1', 'pstate', 'weight')
        # after execution, neuron #1's pstate will be updated
        new_pstate = self.brain.get_neuron_state('1', 'pstate')
        self.assertNotEqual(old_pstate, new_pstate)
        # after execution, neuron #2's input vector will be updated
        new_input2 = self.brain.get_input_values('2')
        self.assertEqual(len(old_input2), 0)
        self.assertEqual(len(new_input2), 1)
        self.assertNotEqual(old_input2, new_input2)
        #print
        #print 'Neuron #2 Input (before): ', old_input2
        #print 'Neuron #2 Input (after): ', new_input2
        # after execution, neuron #2's input vector will be updated
        new_input3 = self.brain.get_input_values('3')
        self.assertEqual(len(old_input2), 0)
        self.assertEqual(len(new_input2), 1)
        self.assertNotEqual(old_input3, new_input3)
        #print 'Neuron #3 Input (before): ', old_input3
        #print 'Neuron #3 Input (after): ', new_input3

    def testExecuteNeuron2(self):
        # set an input into neuron #1
        self.brain.set_input('eye', {'1': 0.15})
        input_vector = self.brain.get_input_values('1')
        self.assertEqual(input_vector, [0.15])
        # get data before execution of neurons
        old_pstates = [self.brain.get_neuron_state(str(ID), state='pstate') 
                       for ID in range(1, 11)]
        # execute neurons #1 to #10
        for ID in self.brain.sequence:
            self.brain.execute_neuron(str(ID), 'pstate', 'weight')
        # get data after execution of neurons
        new_pstates = [self.brain.get_neuron_state(str(ID), state='pstate') 
                       for ID in range(1, 11)]
        self.assertNotEqual(old_pstates, new_pstates)
        print("Execute Neuron 2")
        print('pstates (before): ' + str(old_pstates))
        print('pstates (after): ' + str(new_pstates)) 
        
  
if __name__ == '__main__':
    unittest.main()