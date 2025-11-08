# Escape Room

## Structure of the project

```
EscapeRoom
├── data
│   ├── auth.log
│   ├── dns.cfg
│   ├── final_gate.txt
│   ├── proc_tree.jsonl
│   ├── README_DATA.md
│   └── vault_dump.txt
├── escaperoom
│   ├── engine.py
│   ├── GameState.py
│   ├── rooms
│   │   ├── base.py
│   │   ├── dns.py
│   │   ├── final.py
│   │   ├── intro.py
│   │   ├── malware.py
│   │   ├── soc.py
│   │   └── vault.py
│   ├── transcript.py
│   └── utils.py
├── README.md
├── escape.py
│
├── RunTests.py 
└── tests
    ├── malware_graph_search_results.txt
    ├── Proc_Graph.png
    ├── test_b64decode.py
    ├── test_parse_kv_file.py
    ├── test_read_jsonl.py
    └── TestRegistry.py
```

## Architecture
The project is divided in:
- **Startup script**: Receives players to the game and startup engine/rooms, before passing the controls to the engine.
- **Engine**:  Orchestrate the whole game, receives user input and handles their requests
- **Rooms**: Contains the logic to solve the challenges presented in its room.

## Work Distribution

Initially, the project was divided into 3 important baseline parts, to create a baseline to start working on the rooms themselves and distributed to each of the team members:

- Startup Script (Created by Divya)
- Base Engine (Created by Eldar)
- Transcript Class (Created by João)

With this baseline defined, we had to analyse each room contents to divide the workload fairly according to both its difficulty and the time needed to complete it.
The first room, DNS Room, and Vault Room were both developed by Divya.
The engine, being a bigger task by nature and having the final room logic embedded into it, was still being developed by Eldar, such that only one room was defined to be solved by him: the DNS Room.
Finally, Joao had to develop the remaining rooms: Malware, as it was considered the hardest to code, and DNS Room.

Finally, only documentation remained, which was done by every member of the group, following a common baseline structure to ensure consistency.

João, as the group leader, besides dividing the task, was also in charge of reviewing in depth all code and logic proposed by the group members.
All group members were also encouraged to review each others code.


## Room Logic

### SOC Room 

The room file was read line-by-line, where each line was divided into two parts: process metadata and access metadata, which were analysed separately to understand if they were well-formed.
The process metadata was confirmed to be well-structured through a regex pattern.
The access metadata was split into key-value pairs and detected for missing required data.
Then, if the data had the expected structure, it was analysed taking advantage of the package *ipaddress* available in python's standard libraries.

### DNS Room

The room file were noticed to follow a key=value structure, therefore we wrote a function *parse_kv_file* that in a robust manner, parses this type of files returning a dictionary containing the expected kv pairs.
This allowed for a quick and easy implementation of solving this room using *base64* python package.
However, we found that the expected solution appeared to be corrupted, but it was encrypted using a Caesar's Cypher.
After implementing a function that reverts this cypher, which is the same used to encrypt it, we reached a solution that if the base64 decode fails, we should try to revert this cypher, allowing us to reach the correct plain text.

### Vault Room
Vault Room posed as an easier room as taking advantage of *regex* solved most problems of robustingly parsing this room's data.
With regex's match operation, the values were extracted as groups which allowed an easy a+b=c comparison check.

### Malware Room
Initially, given the processes in the room files, a tree representation consisting of an adjacency-children map was constructed, and as well an auxiliary process_id -> process_metadata map.
Since we had a process-tree, three tree traversing algorithms were implemented: Iterative depth-first and breadth-first search and a recursive depth-first search that searched for a proccess that ran malicious code.
This detection had three requisites to understand if a proccess was considered malicious:
- Does it contain a potentially malicious command: scp and curl?
- If it does, can it extradite data, this is, does in run a post request?
- If it does, is it a leaf node, as specified in the assignment?
If all criteria match, then we consider it a malicious command and the tree search ends, returning the path to that node.


## Tests

In order to test our solution, we did both manual and automated tests.

### Manual tests
Most tests made were manual, were we tested all commands with several relevant inputs, to guarantee it was considered a good solution, we also solved each room with our program and verified by hand each obtained solution guaranteeing that everything worked as expected.
This process was repeated with other group's data, ensuring it worked in all provided scenarios. 
Each tree search algorithm was also tested thoroughly for us to consider it adequate.

### Automatic test

Some automatic tests were also implemented for the functions provided in `./escaperoom/utils.py`.
These tests can be run running the command `python3 RunTests.py`.
They were made following the paradigm that *given X input, then expect Y output*.

#### Test Example
```py
@Test
def givenKVFileWithComments_thenIgnoreComments():
    data = """
    # This is a comment
    key1=value1 # Inline comment
    key2 = value2
    # Another comment
    key3=value3
    """

    expected = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
    }

    result, passed = test_parse_kv_file(data, expected)
    return passed
```
`Running test: givenKVFileWithComments_thenIgnoreComments | Passed`

## AI Acknowledgement

We acknowledge the use of AI to:
- Writting most of documentation with supervision;
- Help understand concepts and assisting in coding.
However, no piece of code written by AI was left to be proof-read/reviewed.
All AI code was also read to thoroughly understand its logic and to guarantee it matched expected logic and functionality.
Tools used include Claude, ChatGPT, Perplexity, Gemini and Github Copilot.