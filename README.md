In this file we will explain how to use the code in this repository, how its structured, and our solution.

# TODO

- Add tests
- Add linting
- finish rooms

# Structure of the project

```
EscapeRoom
├── data
│   ├── auth.log
│   ├── dns.cfg
│   ├── final_gate.txt
│   ├── proc_tree.jsonl
│   ├── README_DATA.md
│   └── vault_dump.txt
├── escape.py
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
├── RunTests.py
├── run.txt
├── save.json
└── tests
    ├── malware_graph_search_results.txt
    ├── Proc_Graph.png
    ├── test_b64decode.py
    ├── test_parse_kv_file.py
    ├── test_read_jsonl.py
    └── TestRegistry.py
`
```

# Work Distribution

Initially, the project was divided into 3 important baseline parts, to create a baseline to start working on the rooms themselves and distributed to each of the team members:

- Startup Script (Created by Divya)
- Base Engine (Created by Eldar)
- Transcript Class (Created by João)

With this baseline defined, we had to analyse each room contents to divide the workload fairly according to both its difficulty and the time needed to complete it.
The first room, DNS Room, and Vault Room were both developed by Divya.
The engine, being a bigger task by nature and having the final room logic embedded into it, was still being developed by Eldar, such that only one room was defined to be solved by him: the DNS Room.
Finally, Joao had to develop the remaining rooms: Malware, as it was considered the hardest to code, and DNS Room.

Finally, only documentation remained, which was done by every member of the group, following a common baseline structure to ensure consistency.
