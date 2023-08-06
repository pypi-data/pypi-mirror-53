# Genie Python SDK
A Python SDK for Intelligent Artifacts' Genie.

## What is Genie?
Genie is a General Evolving Networked Intelligence Engine.  It is an Artificial General Intelligence platform for rapidly building machine intelligence solutions for any problem domain.

Genie requires an account on Intelligent Artifacts.

## What is Genie Python SDK?
This package, Genie Python SDK, is a software development kit for interacting with "genies" and "bottles" from Python.  It provides useful tools and services.

## Install
`pip install ia-genie-sdk`

Provides:

    - GenomeInfo
    - BottleClient
    - BackTesting

#### To use GenomeInfo:

You will need to download your genie's genome file from your Intelligent Artifacts account.

~~~
from ialib.GenomeInfo import Genome
import json

genome_topology = json.loads(genome_json_string)
genome = Genome(genome_topology)
~~~

If you want to have the topology displayed, you need to install cyjupter:

`pip3 install cyjupyter`


##### The useful functions are:
~~~
genome.agent - returns the name of the agent.
    ex: 'focusgenie'

genome.getNodes() - returns 2-tuple of primitives and manipulatives genomic data.

genome.getActions() - returns dictionary of primitives with lists of action IDs.
    ex: {'P1': ['ma23b1323',
                'm390d053c']}

genome.getActionManipulatives() - returns a list of action manipulative IDs.
    ex: ['m390d053c',
         'ma23b1323']

genome.getPrimitiveMap() - returns a dictionary of primitive names to primitive IDs.
    ex: {'P1': 'p464b64bc'}

genome.getManipulativeMap() - returns a dictionary of manipulative IDs to manipulative names.
    ex: {'m390d053c': 'ACTIONPath',
         'ma23b1323': 'ACTIONPath',
         'mcd6d4d68': 'negateContext',
         'm40aaf174': 'vectorFilter',
         'med2ed537': 'vectorPassthrough',
         'm89aa2c7e': 'reduceVectorsBySubtraction'}

genome.display() - graphically displays the topology.
~~~



#### To use BottleClient:

You will need to have an active bottle running on Intelligent Artifacts.  The bottle's information such as 'name' and secrete 'api_key' can be found in your IA account.

If on IA cloud:

~~~
from ialib.BottleClient import BottleClient

bottle_info = {'api_key': 'ABCD-1234',
               'name': 'genie-bottle',
               'domain': 'intelligent-artifacts.com',
               'secure': True}

test_bottle = BottleClient(bottle_info)
test_bottle
~~~


If local:

~~~
from ialib.BottleClient import BottleClient

bottle_info = {'api_key': 'ABCD-1234',
               'name': 'genie-bottle',
               'domain': ':8181',
               'secure': False}

test_bottle = BottleClient(bottle_info)
test_bottle
~~~

Inject your genie's genome into the bottle:

~~~
test_bottle.injectGenome(genome)
~~~

Wait for return status.

Once you have a running genie, set ingress and query nodes by passing the node names in a list:

~~~
test_bottle.setIngressNodes(['P1'])
test_bottle.setQueryNodes(['P1'])
~~~

Send data to bottle:

~~~
data = {"strings": ["Hello"], "vectors": [], "determinants": []}
test_bottle.observe(data)
~~~

Query the bottle nodes:

~~~
print(test_bottle.query('showStatus'))
predictions = test_bottle.query('getPredictions')
~~~

You can also pass GenieMetalanguage data to the genie:

~~~
from ialib.GenieMetalanguage import CLEAR_ALL_MEMORY, CLEAR_WM, LEARN, SET_PREDICTIONS_ON, SET_PREDICTIONS_OFF
test_bottle.observe(LEARN)
~~~

When sending classifications to a genie, it is best practice to send the classification as a singular symbol in the last event of a sequence.  This allows for querying the last event in the prediction's 'future' field for the answer.  The classification, though, should be sent to all the query nodes along with the ingress nodes.  The `observeClassification` function of the `BottleClient` class does that for us:

~~~
data = {"strings": ["World!"], "vectors": [], "determinants": []}
test_bottle.observeClassification(data)
~~~

#### To use Backtesting:

There are 3 built-in backtesting reports:
    - classification:
        - Train and predict a string value to be a classification of observed data.
    - utility - polarity:
        - Polarity is basically a +/- binary classification test using the prediction's 'utility' value.  It scores correct if the polarity of the prediction matches the polarity of the expected.
    - utility - value:
        - Value tests for the actual predicted value against the expected and scores correct if within a provided `tolerance_threshold`.

For each, the observed data can be a sequence of one or more events, containing any vectors or strings.