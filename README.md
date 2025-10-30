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
