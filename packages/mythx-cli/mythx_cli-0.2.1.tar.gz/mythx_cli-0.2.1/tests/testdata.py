from mythx_models.response import (
    AnalysisInputResponse,
    AnalysisListResponse,
    AnalysisStatusResponse,
    AnalysisSubmissionResponse,
    DetectedIssuesResponse,
    VersionResponse,
)

VERSION_RESPONSE_OBJ = VersionResponse.from_dict(
    {
        "api": "v1.4.34.4",
        "maru": "0.5.3",
        "mythril": "0.21.14",
        "harvey": "0.0.33",
        "hash": "6e0035da873e809e90eab4665e3d19d6",
    }
)

VERSION_RESPONSE_SIMPLE = """API: v1.4.34.4
Harvey: 0.0.33
Maru: 0.5.3
Mythril: 0.21.14
Hashed: 6e0035da873e809e90eab4665e3d19d6
"""

VERSION_RESPONSE_TABLE = """╒═════════╤══════════════════════════════════╕
│ Api     │ v1.4.34.4                        │
├─────────┼──────────────────────────────────┤
│ Maru    │ 0.5.3                            │
├─────────┼──────────────────────────────────┤
│ Mythril │ 0.21.14                          │
├─────────┼──────────────────────────────────┤
│ Harvey  │ 0.0.33                           │
├─────────┼──────────────────────────────────┤
│ Hash    │ 6e0035da873e809e90eab4665e3d19d6 │
╘═════════╧══════════════════════════════════╛
"""

STATUS_RESPONSE_OBJ = AnalysisStatusResponse.from_dict(
    {
        "uuid": "ab9092f7-54d0-480f-9b63-1bb1508280e2",
        "apiVersion": "v1.4.33-1-g1a235db",
        "mythrilVersion": "0.21.14",
        "harveyVersion": "0.0.34",
        "maruVersion": "0.5.4",
        "queueTime": 507,
        "runTime": 30307,
        "status": "Finished",
        "submittedAt": "2019-09-05T20:34:27.606Z",
        "submittedBy": "5d6fca7fef1fc700129b6efa",
        "clientToolName": "pythx",
    }
)
STATUS_RESPONSE_SIMPLE = """UUID: ab9092f7-54d0-480f-9b63-1bb1508280e2
Submitted at: 2019-09-05 20:34:27.606000+00:00
Status: Finished

"""

STATUS_RESPONSE_TABLE = """╒════════════════╤══════════════════════════════════════╕
│ uuid           │ ab9092f7-54d0-480f-9b63-1bb1508280e2 │
├────────────────┼──────────────────────────────────────┤
│ apiVersion     │ v1.4.33-1-g1a235db                   │
├────────────────┼──────────────────────────────────────┤
│ mythrilVersion │ 0.21.14                              │
├────────────────┼──────────────────────────────────────┤
│ harveyVersion  │ 0.0.34                               │
├────────────────┼──────────────────────────────────────┤
│ maruVersion    │ 0.5.4                                │
├────────────────┼──────────────────────────────────────┤
│ queueTime      │ 507                                  │
├────────────────┼──────────────────────────────────────┤
│ runTime        │ 30307                                │
├────────────────┼──────────────────────────────────────┤
│ status         │ Finished                             │
├────────────────┼──────────────────────────────────────┤
│ submittedAt    │ 2019-09-05T20:34:27.606Z             │
├────────────────┼──────────────────────────────────────┤
│ submittedBy    │ 5d6fca7fef1fc700129b6efa             │
├────────────────┼──────────────────────────────────────┤
│ clientToolName │ pythx                                │
╘════════════════╧══════════════════════════════════════╛
"""


LIST_RESPONSE_OBJ = AnalysisListResponse.from_dict(
    {
        "analyses": [
            {
                "uuid": "ed6b2347-68b7-4ef3-b85c-4340ae404867",
                "apiVersion": "v1.4.33-37-g0fb1a8f",
                "mythrilVersion": "0.21.14",
                "harveyVersion": "0.0.34",
                "maruVersion": "0.5.4",
                "queueTime": 1400,
                "runTime": 4267,
                "status": "Finished",
                "submittedAt": "2019-09-10T17:15:11.267Z",
                "submittedBy": "5d6fca7fef1fc700129b6efa",
                "clientToolName": "pythx",
            },
            {
                "uuid": "e6566fc9-ebc1-4d04-ae5d-6f3b1873290a",
                "apiVersion": "v1.4.33-37-g0fb1a8f",
                "mythrilVersion": "0.21.14",
                "harveyVersion": "0.0.34",
                "maruVersion": "0.5.4",
                "queueTime": 2015,
                "runTime": 28427,
                "status": "Finished",
                "submittedAt": "2019-09-10T17:15:10.645Z",
                "submittedBy": "5d6fca7fef1fc700129b6efa",
                "clientToolName": "pythx",
            },
            {
                "uuid": "b87f0174-ef09-4fac-9d3c-97c3fdf01782",
                "apiVersion": "v1.4.33-37-g0fb1a8f",
                "mythrilVersion": "0.21.14",
                "harveyVersion": "0.0.34",
                "maruVersion": "0.5.4",
                "queueTime": 2816,
                "runTime": 52405,
                "status": "Finished",
                "submittedAt": "2019-09-10T17:15:09.836Z",
                "submittedBy": "5d6fca7fef1fc700129b6efa",
                "clientToolName": "pythx",
            },
            {
                "uuid": "2056caf6-25d7-4ce8-a633-d10a8746d5dd",
                "apiVersion": "v1.4.33-37-g0fb1a8f",
                "mythrilVersion": "0.21.14",
                "harveyVersion": "0.0.34",
                "maruVersion": "0.5.4",
                "queueTime": 80698393,
                "runTime": -80698393,
                "status": "Finished",
                "submittedAt": "2019-09-10T17:12:42.341Z",
                "submittedBy": "5d6fca7fef1fc700129b6efa",
                "clientToolName": "pythx",
            },
            {
                "uuid": "63eb5611-ba4b-46e8-9e40-f735a0b86fd9",
                "apiVersion": "v1.4.33-37-g0fb1a8f",
                "mythrilVersion": "0.21.14",
                "harveyVersion": "0.0.34",
                "maruVersion": "0.5.4",
                "queueTime": 1158,
                "runTime": 130267,
                "status": "Finished",
                "submittedAt": "2019-09-10T17:12:41.645Z",
                "submittedBy": "5d6fca7fef1fc700129b6efa",
                "clientToolName": "pythx",
            },
        ],
        "total": 5,
    }
)
LIST_RESPONSE_SIMPLE = """UUID: ed6b2347-68b7-4ef3-b85c-4340ae404867
Submitted at: 2019-09-10 17:15:11.267000+00:00
Status: Finished

UUID: e6566fc9-ebc1-4d04-ae5d-6f3b1873290a
Submitted at: 2019-09-10 17:15:10.645000+00:00
Status: Finished

UUID: b87f0174-ef09-4fac-9d3c-97c3fdf01782
Submitted at: 2019-09-10 17:15:09.836000+00:00
Status: Finished

UUID: 2056caf6-25d7-4ce8-a633-d10a8746d5dd
Submitted at: 2019-09-10 17:12:42.341000+00:00
Status: Finished

UUID: 63eb5611-ba4b-46e8-9e40-f735a0b86fd9
Submitted at: 2019-09-10 17:12:41.645000+00:00
Status: Finished

"""

LIST_RESPONSE_TABLE = """╒══════════════════════════════════════╤══════════╤═══════╤══════════════════════════════════╕
│ ed6b2347-68b7-4ef3-b85c-4340ae404867 │ Finished │ pythx │ 2019-09-10 17:15:11.267000+00:00 │
├──────────────────────────────────────┼──────────┼───────┼──────────────────────────────────┤
│ e6566fc9-ebc1-4d04-ae5d-6f3b1873290a │ Finished │ pythx │ 2019-09-10 17:15:10.645000+00:00 │
├──────────────────────────────────────┼──────────┼───────┼──────────────────────────────────┤
│ b87f0174-ef09-4fac-9d3c-97c3fdf01782 │ Finished │ pythx │ 2019-09-10 17:15:09.836000+00:00 │
├──────────────────────────────────────┼──────────┼───────┼──────────────────────────────────┤
│ 2056caf6-25d7-4ce8-a633-d10a8746d5dd │ Finished │ pythx │ 2019-09-10 17:12:42.341000+00:00 │
├──────────────────────────────────────┼──────────┼───────┼──────────────────────────────────┤
│ 63eb5611-ba4b-46e8-9e40-f735a0b86fd9 │ Finished │ pythx │ 2019-09-10 17:12:41.645000+00:00 │
╘══════════════════════════════════════╧══════════╧═══════╧══════════════════════════════════╛
"""

SUBMISSION_RESPONSE_OBJ = AnalysisSubmissionResponse.from_dict(
    {
        "apiVersion": "v1.3.0",
        "harveyVersion": "v0.1.0",
        "maruVersion": "v0.2.0",
        "mythrilVersion": "0.19.11",
        "queueTime": 0,
        "status": "Queued",
        "submittedAt": "2019-01-10T01:29:38.410Z",
        "submittedBy": "000008544b0aa00010a91111",
        "uuid": "ab9092f7-54d0-480f-9b63-1bb1508280e2",
    }
)

ARTIFACT_DATA = {
    "contractName": "IApplication",
    "abi": [
        {
            "constant": False,
            "inputs": [{"name": "data", "type": "bytes"}],
            "name": "initialize",
            "outputs": [],
            "payable": False,
            "stateMutability": "nonpayable",
            "type": "function",
        }
    ],
    "metadata": "",
    "bytecode": "0x",
    "deployedBytecode": "0x",
    "sourceMap": "",
    "deployedSourceMap": "",
    "source": "pragma solidity ^0.4.18;\n\n\ncontract IApplication {\n  function initialize(bytes data) public;\n}\n",
    "sourcePath": "/home/spoons/diligence/mythx-qa/land/contracts/upgradable/IApplication.sol",
    "ast": {
        "absolutePath": "/home/spoons/diligence/mythx-qa/land/contracts/upgradable/IApplication.sol",
        "exportedSymbols": {"IApplication": [3050]},
        "id": 3051,
        "nodeType": "SourceUnit",
        "nodes": [
            {
                "id": 3044,
                "literals": ["solidity", "^", "0.4", ".18"],
                "nodeType": "PragmaDirective",
                "src": "0:24:9",
            },
            {
                "baseContracts": [],
                "contractDependencies": [],
                "contractKind": "contract",
                "documentation": None,
                "fullyImplemented": False,
                "id": 3050,
                "linearizedBaseContracts": [3050],
                "name": "IApplication",
                "nodeType": "ContractDefinition",
                "nodes": [
                    {
                        "body": None,
                        "documentation": None,
                        "id": 3049,
                        "implemented": False,
                        "isConstructor": False,
                        "isDeclaredConst": False,
                        "modifiers": [],
                        "name": "initialize",
                        "nodeType": "FunctionDefinition",
                        "parameters": {
                            "id": 3047,
                            "nodeType": "ParameterList",
                            "parameters": [
                                {
                                    "constant": False,
                                    "id": 3046,
                                    "name": "data",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 3049,
                                    "src": "73:10:9",
                                    "stateVariable": False,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_bytes_memory_ptr",
                                        "typeString": "bytes",
                                    },
                                    "typeName": {
                                        "id": 3045,
                                        "name": "bytes",
                                        "nodeType": "ElementaryTypeName",
                                        "src": "73:5:9",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_bytes_storage_ptr",
                                            "typeString": "bytes",
                                        },
                                    },
                                    "value": None,
                                    "visibility": "internal",
                                }
                            ],
                            "src": "72:12:9",
                        },
                        "payable": False,
                        "returnParameters": {
                            "id": 3048,
                            "nodeType": "ParameterList",
                            "parameters": [],
                            "src": "91:0:9",
                        },
                        "scope": 3050,
                        "src": "53:39:9",
                        "stateMutability": "nonpayable",
                        "superFunction": None,
                        "visibility": "public",
                    }
                ],
                "scope": 3051,
                "src": "27:67:9",
            },
        ],
        "src": "0:95:9",
    },
    "legacyAST": {
        "absolutePath": "/home/spoons/diligence/mythx-qa/land/contracts/upgradable/IApplication.sol",
        "exportedSymbols": {"IApplication": [3050]},
        "id": 3051,
        "nodeType": "SourceUnit",
        "nodes": [
            {
                "id": 3044,
                "literals": ["solidity", "^", "0.4", ".18"],
                "nodeType": "PragmaDirective",
                "src": "0:24:9",
            },
            {
                "baseContracts": [],
                "contractDependencies": [],
                "contractKind": "contract",
                "documentation": None,
                "fullyImplemented": False,
                "id": 3050,
                "linearizedBaseContracts": [3050],
                "name": "IApplication",
                "nodeType": "ContractDefinition",
                "nodes": [
                    {
                        "body": None,
                        "documentation": None,
                        "id": 3049,
                        "implemented": False,
                        "isConstructor": False,
                        "isDeclaredConst": False,
                        "modifiers": [],
                        "name": "initialize",
                        "nodeType": "FunctionDefinition",
                        "parameters": {
                            "id": 3047,
                            "nodeType": "ParameterList",
                            "parameters": [
                                {
                                    "constant": False,
                                    "id": 3046,
                                    "name": "data",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 3049,
                                    "src": "73:10:9",
                                    "stateVariable": False,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_bytes_memory_ptr",
                                        "typeString": "bytes",
                                    },
                                    "typeName": {
                                        "id": 3045,
                                        "name": "bytes",
                                        "nodeType": "ElementaryTypeName",
                                        "src": "73:5:9",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_bytes_storage_ptr",
                                            "typeString": "bytes",
                                        },
                                    },
                                    "value": None,
                                    "visibility": "internal",
                                }
                            ],
                            "src": "72:12:9",
                        },
                        "payable": False,
                        "returnParameters": {
                            "id": 3048,
                            "nodeType": "ParameterList",
                            "parameters": [],
                            "src": "91:0:9",
                        },
                        "scope": 3050,
                        "src": "53:39:9",
                        "stateMutability": "nonpayable",
                        "superFunction": None,
                        "visibility": "public",
                    }
                ],
                "scope": 3051,
                "src": "27:67:9",
            },
        ],
        "src": "0:95:9",
    },
    "compiler": {"name": "solc", "version": "0.4.24+commit.e67f0147.Emscripten.clang"},
    "networks": {},
    "schemaVersion": "3.0.8",
    "updatedAt": "2019-04-30T11:34:15.037Z",
    "devdoc": {"methods": {}},
    "userdoc": {"methods": {}},
}


ISSUES_RESPONSE_OBJ = DetectedIssuesResponse.from_dict(
    [
        {
            "issues": [
                {
                    "swcID": "SWC-110",
                    "swcTitle": "Assert Violation",
                    "description": {
                        "head": "A reachable exception has been detected.",
                        "tail": "It is possible to trigger an exception (opcode 0xfe). Exceptions can be caused by type errors, division by zero, out-of-bounds array access, or assert violations. Note that explicit `assert()` should only be used to check invariants. Use `require()` for regular input checking.",
                    },
                    "severity": "Low",
                    "locations": [
                        {
                            "sourceMap": "454:1:1",
                            "sourceType": "raw-bytecode",
                            "sourceFormat": "evm-byzantium-bytecode",
                            "sourceList": [
                                "0xc4fb652765fbc8c62ef9e87524c33e75cec4800f5f926c9b92bb65a8f344516c",
                                "0x450f10bb4c2c7c13bba9bee136d5dcffc96afdef00d12b3b9398f7c32a7571c6",
                            ],
                        },
                        {
                            "sourceMap": "812:50:0",
                            "sourceType": "solidity-file",
                            "sourceFormat": "text",
                            "sourceList": [
                                "/home/spoons/diligence/mythx-qa/land/contracts/estate/EstateStorage.sol"
                            ],
                        },
                    ],
                    "extra": {
                        "discoveryTime": 5723484754,
                        "testCases": [
                            {
                                "initialState": {
                                    "accounts": {
                                        "0x901d12ebe1b195e5aa8748e62bd7734ae19b51f": {
                                            "balance": "0x0",
                                            "code": "6080604052600436106100775763ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166307ecec3e811461007c5780630a354fce146100c45780633970bfd3146100ee5780637b103999146101095780639d40b850146101475780639f813b1b1461015f575b600080fd5b34801561008857600080fd5b506100b073ffffffffffffffffffffffffffffffffffffffff6004358116906024351661017a565b604080519115158252519081900360200190f35b3480156100d057600080fd5b506100dc60043561019a565b60408051918252519081900360200190f35b3480156100fa57600080fd5b506100dc6004356024356101ac565b34801561011557600080fd5b5061011e6101dc565b6040805173ffffffffffffffffffffffffffffffffffffffff9092168252519081900360200190f35b34801561015357600080fd5b5061011e6004356101f8565b34801561016b57600080fd5b506100dc600435602435610220565b600660209081526000928352604080842090915290825290205460ff1681565b60026020526000908152604090205481565b6001602052816000526040600020818154811015156101c757fe5b90600052602060002001600091509150505481565b60005473ffffffffffffffffffffffffffffffffffffffff1681565b60056020526000908152604090205473ffffffffffffffffffffffffffffffffffffffff1681565b6003602090815260009283526040808420909152908252902054815600a165627a7a72305820f64a07ca79d7ea541c6da153a5e58913679321b2cc8435fdddbd0735083dba550029",
                                            "nonce": 0,
                                            "storage": {},
                                        },
                                        "0xaffeaffeaffeaffeaffeaffeaffeaffeaffeaffe": {
                                            "balance": "0x1",
                                            "code": "",
                                            "nonce": 0,
                                            "storage": {},
                                        },
                                        "0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef": {
                                            "balance": "0x0",
                                            "code": "",
                                            "nonce": 0,
                                            "storage": {},
                                        },
                                    }
                                },
                                "steps": [
                                    {
                                        "address": "",
                                        "blockCoinbase": "0xcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcb",
                                        "blockDifficulty": "0xa7d7343662e26",
                                        "blockGasLimit": "0x7d0000",
                                        "blockNumber": "0x66e393",
                                        "blockTime": "0x5bfa4639",
                                        "gasLimit": "0x7d000",
                                        "gasPrice": "0x773594000",
                                        "input": "0x608060405234801561001057600080fd5b50610269806100206000396000f3006080604052600436106100775763ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166307ecec3e811461007c5780630a354fce146100c45780633970bfd3146100ee5780637b103999146101095780639d40b850146101475780639f813b1b1461015f575b600080fd5b34801561008857600080fd5b506100b073ffffffffffffffffffffffffffffffffffffffff6004358116906024351661017a565b604080519115158252519081900360200190f35b3480156100d057600080fd5b506100dc60043561019a565b60408051918252519081900360200190f35b3480156100fa57600080fd5b506100dc6004356024356101ac565b34801561011557600080fd5b5061011e6101dc565b6040805173ffffffffffffffffffffffffffffffffffffffff9092168252519081900360200190f35b34801561015357600080fd5b5061011e6004356101f8565b34801561016b57600080fd5b506100dc600435602435610220565b600660209081526000928352604080842090915290825290205460ff1681565b60026020526000908152604090205481565b6001602052816000526040600020818154811015156101c757fe5b90600052602060002001600091509150505481565b60005473ffffffffffffffffffffffffffffffffffffffff1681565b60056020526000908152604090205473ffffffffffffffffffffffffffffffffffffffff1681565b6003602090815260009283526040808420909152908252902054815600a165627a7a72305820f64a07ca79d7ea541c6da153a5e58913679321b2cc8435fdddbd0735083dba550029",
                                        "name": "unknown",
                                        "origin": "0xaffeaffeaffeaffeaffeaffeaffeaffeaffeaffe",
                                        "value": "0x0",
                                    },
                                    {
                                        "address": "0x901d12ebe1b195e5aa8748e62bd7734ae19b51f",
                                        "blockCoinbase": "0xcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcbcb",
                                        "blockDifficulty": "0xa7d7343662e26",
                                        "blockGasLimit": "0x7d0000",
                                        "blockNumber": "0x66e393",
                                        "blockTime": "0x5bfa4639",
                                        "gasLimit": "0x7d000",
                                        "gasPrice": "0x773594000",
                                        "input": "0x3970bfd3",
                                        "name": "unknown",
                                        "origin": "0xaffeaffeaffeaffeaffeaffeaffeaffeaffeaffe",
                                        "value": "0x0",
                                    },
                                ],
                            },
                            {
                                "initialState": {
                                    "accounts": {
                                        "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0": {
                                            "nonce": 0,
                                            "balance": "0x00000000000000000000000000000000000000ffffffffffffffffffffffffff",
                                            "code": "",
                                            "storage": {},
                                        },
                                        "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1": {
                                            "nonce": 1,
                                            "balance": "0x0000000000000000000000000000000000000000000000000000000000000000",
                                            "code": "",
                                            "storage": {},
                                        },
                                        "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2": {
                                            "nonce": 1,
                                            "balance": "0x00000000000000000000000000000000000000ffffffffffffffffffffffffff",
                                            "code": "",
                                            "storage": {},
                                        },
                                        "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa3": {
                                            "nonce": 1,
                                            "balance": "0x00000000000000000000000000000000000000ffffffffffffffffffffffffff",
                                            "code": "0x00",
                                            "storage": {},
                                        },
                                        "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa4": {
                                            "nonce": 1,
                                            "balance": "0x00000000000000000000000000000000000000ffffffffffffffffffffffffff",
                                            "code": "0xfd",
                                            "storage": {},
                                        },
                                        "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa5": {
                                            "nonce": 1,
                                            "balance": "0x00000000000000000000000000000000000000ffffffffffffffffffffffffff",
                                            "code": "0x608060405260005600a165627a7a72305820466f8a1bdae15c60b8e998fe04836ef505803cfbd8edd29bd4679531357576530029",
                                            "storage": {},
                                        },
                                        "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa6": {
                                            "nonce": 1,
                                            "balance": "0x00000000000000000000000000000000000000ffffffffffffffffffffffffff",
                                            "code": "0x608060405273aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa63081146038578073ffffffffffffffffffffffffffffffffffffffff16ff5b5000fea165627a7a723058205e8b906b72ad42c69b05acf4542283b6080ae82562bc74baac467daac2fb0e0e0029",
                                            "storage": {},
                                        },
                                        "0xaffeaffeaffeaffeaffeaffeaffeaffeaffeaffe": {
                                            "nonce": 0,
                                            "balance": "0x0000000000000000000000000000000000ffffffffffffffffffffffffffffff",
                                            "code": "",
                                            "storage": {},
                                        },
                                    }
                                },
                                "steps": [
                                    {
                                        "address": "",
                                        "gasLimit": "0xffffff",
                                        "gasPrice": "0x773594000",
                                        "input": "0x608060405234801561001057600080fd5b50610269806100206000396000f3006080604052600436106100775763ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166307ecec3e811461007c5780630a354fce146100c45780633970bfd3146100ee5780637b103999146101095780639d40b850146101475780639f813b1b1461015f575b600080fd5b34801561008857600080fd5b506100b073ffffffffffffffffffffffffffffffffffffffff6004358116906024351661017a565b604080519115158252519081900360200190f35b3480156100d057600080fd5b506100dc60043561019a565b60408051918252519081900360200190f35b3480156100fa57600080fd5b506100dc6004356024356101ac565b34801561011557600080fd5b5061011e6101dc565b6040805173ffffffffffffffffffffffffffffffffffffffff9092168252519081900360200190f35b34801561015357600080fd5b5061011e6004356101f8565b34801561016b57600080fd5b506100dc600435602435610220565b600660209081526000928352604080842090915290825290205460ff1681565b60026020526000908152604090205481565b6001602052816000526040600020818154811015156101c757fe5b90600052602060002001600091509150505481565b60005473ffffffffffffffffffffffffffffffffffffffff1681565b60056020526000908152604090205473ffffffffffffffffffffffffffffffffffffffff1681565b6003602090815260009283526040808420909152908252902054815600a165627a7a72305820f64a07ca79d7ea541c6da153a5e58913679321b2cc8435fdddbd0735083dba550029",
                                        "origin": "0xaffeaffeaffeaffeaffeaffeaffeaffeaffeaffe",
                                        "value": "0x0",
                                        "blockCoinbase": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0",
                                        "blockDifficulty": "0xa7d7343662e26",
                                        "blockGasLimit": "0xffffff",
                                        "blockNumber": "0x661a55",
                                        "blockTime": "0x5be99aa8",
                                    },
                                    {
                                        "address": "0x0901d12ebe1b195e5aa8748e62bd7734ae19b51f",
                                        "gasLimit": "0x7d000",
                                        "gasPrice": "0x773594000",
                                        "input": "0x3970bfd30000000000000000000000000000000000000011000000000000000000000000000000000000000000000000000000000000000000000000",
                                        "origin": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0",
                                        "value": "0x0",
                                        "blockCoinbase": "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0",
                                        "blockDifficulty": "0xa7d7343662e26",
                                        "blockGasLimit": "0x7d0000",
                                        "blockNumber": "0x68621c",
                                        "blockTime": "0x5be99aa8",
                                    },
                                ],
                            },
                        ],
                        "toolName": "mythril",
                    },
                },
                {
                    "swcID": "",
                    "swcTitle": "",
                    "description": {
                        "head": "Upgrade to MythX Pro to unlock the ability to test for even more vulnerabilities, perform deeper security analysis, and more. https://mythx.io/plans",
                        "tail": "Warning: Free mode only detects certain types of smart contract vulnerabilities. Your contract may still be unsafe. Upgrade to MythX Pro to unlock the ability to test for even more vulnerabilities, perform deeper security analysis, and more. https://mythx.io/plans",
                    },
                    "severity": "Low",
                    "locations": [],
                    "extra": {},
                },
            ],
            "sourceType": "solidity-file",
            "sourceFormat": "text",
            "sourceList": [
                "/home/spoons/diligence/mythx-qa/land/contracts/estate/EstateStorage.sol"
            ],
            "meta": {
                "selectedCompiler": "Unknown",
                "coveredPaths": 14,
                "coveredInstructions": 315,
            },
        }
    ]
)
INPUT_RESPONSE_OBJ = AnalysisInputResponse.from_dict(
    {
        "contractName": "EstateStorage",
        "bytecode": "0x608060405234801561001057600080fd5b50610269806100206000396000f3006080604052600436106100775763ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166307ecec3e811461007c5780630a354fce146100c45780633970bfd3146100ee5780637b103999146101095780639d40b850146101475780639f813b1b1461015f575b600080fd5b34801561008857600080fd5b506100b073ffffffffffffffffffffffffffffffffffffffff6004358116906024351661017a565b604080519115158252519081900360200190f35b3480156100d057600080fd5b506100dc60043561019a565b60408051918252519081900360200190f35b3480156100fa57600080fd5b506100dc6004356024356101ac565b34801561011557600080fd5b5061011e6101dc565b6040805173ffffffffffffffffffffffffffffffffffffffff9092168252519081900360200190f35b34801561015357600080fd5b5061011e6004356101f8565b34801561016b57600080fd5b506100dc600435602435610220565b600660209081526000928352604080842090915290825290205460ff1681565b60026020526000908152604090205481565b6001602052816000526040600020818154811015156101c757fe5b90600052602060002001600091509150505481565b60005473ffffffffffffffffffffffffffffffffffffffff1681565b60056020526000908152604090205473ffffffffffffffffffffffffffffffffffffffff1681565b6003602090815260009283526040808420909152908252902054815600a165627a7a72305820f64a07ca79d7ea541c6da153a5e58913679321b2cc8435fdddbd0735083dba550029",
        "sourceMap": "482:970:0:-;;;;8:9:-1;5:2;;;30:1;27;20:12;5:2;482:970:0;;;;;;;",
        "deployedBytecode": "0x6080604052600436106100775763ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166307ecec3e811461007c5780630a354fce146100c45780633970bfd3146100ee5780637b103999146101095780639d40b850146101475780639f813b1b1461015f575b600080fd5b34801561008857600080fd5b506100b073ffffffffffffffffffffffffffffffffffffffff6004358116906024351661017a565b604080519115158252519081900360200190f35b3480156100d057600080fd5b506100dc60043561019a565b60408051918252519081900360200190f35b3480156100fa57600080fd5b506100dc6004356024356101ac565b34801561011557600080fd5b5061011e6101dc565b6040805173ffffffffffffffffffffffffffffffffffffffff9092168252519081900360200190f35b34801561015357600080fd5b5061011e6004356101f8565b34801561016b57600080fd5b506100dc600435602435610220565b600660209081526000928352604080842090915290825290205460ff1681565b60026020526000908152604090205481565b6001602052816000526040600020818154811015156101c757fe5b90600052602060002001600091509150505481565b60005473ffffffffffffffffffffffffffffffffffffffff1681565b60056020526000908152604090205473ffffffffffffffffffffffffffffffffffffffff1681565b6003602090815260009283526040808420909152908252902054815600a165627a7a72305820f64a07ca79d7ea541c6da153a5e58913679321b2cc8435fdddbd0735083dba550029",
        "deployedSourceMap": "482:970:0:-;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;1383:65;;8:9:-1;5:2;;;30:1;27;20:12;5:2;-1:-1;1383:65:0;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;915:47;;8:9:-1;5:2;;;30:1;27;20:12;5:2;-1:-1;915:47:0;;;;;;;;;;;;;;;;;;;;;812:50;;8:9:-1;5:2;;;30:1;27;20:12;5:2;-1:-1;812:50:0;;;;;;;728:28;;8:9:-1;5:2;;;30:1;27;20:12;5:2;728:28:0;;;;;;;;;;;;;;;;;;;;;;;1235:50;;8:9:-1;5:2;;;30:1;27;20:12;5:2;-1:-1;1235:50:0;;;;;1053:70;;8:9:-1;5:2;;;30:1;27;20:12;5:2;-1:-1;1053:70:0;;;;;;;1383:65;;;;;;;;;;;;;;;;;;;;;;;;;;:::o;915:47::-;;;;;;;;;;;;;:::o;812:50::-;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;:::o;728:28::-;;;;;;:::o;1235:50::-;;;;;;;;;;;;;;;:::o;1053:70::-;;;;;;;;;;;;;;;;;;;;;;;;:::o",
        "mainSource": "/home/spoons/diligence/mythx-qa/land/contracts/estate/EstateStorage.sol",
        "sources": {
            "/home/spoons/diligence/mythx-qa/land/contracts/estate/EstateStorage.sol": {
                "source": 'pragma solidity ^0.4.23;\n\n\ncontract LANDRegistry {\n  function decodeTokenId(uint value) external pure returns (int, int);\n  function updateLandData(int x, int y, string data) external;\n  function setUpdateOperator(uint256 assetId, address operator) external;\n  function ping() public;\n  function ownerOf(uint256 tokenId) public returns (address);\n  function safeTransferFrom(address, address, uint256) public;\n  function updateOperator(uint256 landId) public returns (address);\n}\n\n\ncontract EstateStorage {\n  bytes4 internal constant InterfaceId_GetMetadata = bytes4(keccak256("getMetadata(uint256)"));\n  bytes4 internal constant InterfaceId_VerifyFingerprint = bytes4(\n    keccak256("verifyFingerprint(uint256,bytes)")\n  );\n\n  LANDRegistry public registry;\n\n  // From Estate to list of owned LAND ids (LANDs)\n  mapping(uint256 => uint256[]) public estateLandIds;\n\n  // From LAND id (LAND) to its owner Estate id\n  mapping(uint256 => uint256) public landIdEstate;\n\n  // From Estate id to mapping of LAND id to index on the array above (estateLandIds)\n  mapping(uint256 => mapping(uint256 => uint256)) public estateLandIndex;\n\n  // Metadata of the Estate\n  mapping(uint256 => string) internal estateData;\n\n  // Operator of the Estate\n  mapping (uint256 => address) public updateOperator;\n\n  // From account to mapping of operator to bool whether is allowed to update content or not\n  mapping(address => mapping(address => bool)) public updateManager;\n\n}\n',
                "ast": {
                    "absolutePath": "/home/spoons/diligence/mythx-qa/land/contracts/estate/EstateStorage.sol",
                    "exportedSymbols": {
                        "EstateStorage": [1221],
                        "LANDRegistry": [1175],
                    },
                    "id": 1222,
                    "nodeType": "SourceUnit",
                    "nodes": [
                        {
                            "id": 1123,
                            "literals": ["solidity", "^", "0.4", ".23"],
                            "nodeType": "PragmaDirective",
                            "src": "0:24:2",
                        },
                        {
                            "baseContracts": [],
                            "contractDependencies": [],
                            "contractKind": "contract",
                            "documentation": None,
                            "fullyImplemented": False,
                            "id": 1175,
                            "linearizedBaseContracts": [1175],
                            "name": "LANDRegistry",
                            "nodeType": "ContractDefinition",
                            "nodes": [
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1132,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": True,
                                    "modifiers": [],
                                    "name": "decodeTokenId",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1126,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1125,
                                                "name": "value",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1132,
                                                "src": "76:10:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                                "typeName": {
                                                    "id": 1124,
                                                    "name": "uint",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "76:4:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_uint256",
                                                        "typeString": "uint256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            }
                                        ],
                                        "src": "75:12:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1131,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1128,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1132,
                                                "src": "111:3:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_int256",
                                                    "typeString": "int256",
                                                },
                                                "typeName": {
                                                    "id": 1127,
                                                    "name": "int",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "111:3:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_int256",
                                                        "typeString": "int256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                            {
                                                "constant": False,
                                                "id": 1130,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1132,
                                                "src": "116:3:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_int256",
                                                    "typeString": "int256",
                                                },
                                                "typeName": {
                                                    "id": 1129,
                                                    "name": "int",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "116:3:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_int256",
                                                        "typeString": "int256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                        ],
                                        "src": "110:10:2",
                                    },
                                    "scope": 1175,
                                    "src": "53:68:2",
                                    "stateMutability": "pure",
                                    "superFunction": None,
                                    "visibility": "external",
                                },
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1141,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": False,
                                    "modifiers": [],
                                    "name": "updateLandData",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1139,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1134,
                                                "name": "x",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1141,
                                                "src": "148:5:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_int256",
                                                    "typeString": "int256",
                                                },
                                                "typeName": {
                                                    "id": 1133,
                                                    "name": "int",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "148:3:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_int256",
                                                        "typeString": "int256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                            {
                                                "constant": False,
                                                "id": 1136,
                                                "name": "y",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1141,
                                                "src": "155:5:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_int256",
                                                    "typeString": "int256",
                                                },
                                                "typeName": {
                                                    "id": 1135,
                                                    "name": "int",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "155:3:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_int256",
                                                        "typeString": "int256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                            {
                                                "constant": False,
                                                "id": 1138,
                                                "name": "data",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1141,
                                                "src": "162:11:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_string_calldata_ptr",
                                                    "typeString": "string",
                                                },
                                                "typeName": {
                                                    "id": 1137,
                                                    "name": "string",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "162:6:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_string_storage_ptr",
                                                        "typeString": "string",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                        ],
                                        "src": "147:27:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1140,
                                        "nodeType": "ParameterList",
                                        "parameters": [],
                                        "src": "183:0:2",
                                    },
                                    "scope": 1175,
                                    "src": "124:60:2",
                                    "stateMutability": "nonpayable",
                                    "superFunction": None,
                                    "visibility": "external",
                                },
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1148,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": False,
                                    "modifiers": [],
                                    "name": "setUpdateOperator",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1146,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1143,
                                                "name": "assetId",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1148,
                                                "src": "214:15:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                                "typeName": {
                                                    "id": 1142,
                                                    "name": "uint256",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "214:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_uint256",
                                                        "typeString": "uint256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                            {
                                                "constant": False,
                                                "id": 1145,
                                                "name": "operator",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1148,
                                                "src": "231:16:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_address",
                                                    "typeString": "address",
                                                },
                                                "typeName": {
                                                    "id": 1144,
                                                    "name": "address",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "231:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_address",
                                                        "typeString": "address",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                        ],
                                        "src": "213:35:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1147,
                                        "nodeType": "ParameterList",
                                        "parameters": [],
                                        "src": "257:0:2",
                                    },
                                    "scope": 1175,
                                    "src": "187:71:2",
                                    "stateMutability": "nonpayable",
                                    "superFunction": None,
                                    "visibility": "external",
                                },
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1151,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": False,
                                    "modifiers": [],
                                    "name": "ping",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1149,
                                        "nodeType": "ParameterList",
                                        "parameters": [],
                                        "src": "274:2:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1150,
                                        "nodeType": "ParameterList",
                                        "parameters": [],
                                        "src": "283:0:2",
                                    },
                                    "scope": 1175,
                                    "src": "261:23:2",
                                    "stateMutability": "nonpayable",
                                    "superFunction": None,
                                    "visibility": "public",
                                },
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1158,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": False,
                                    "modifiers": [],
                                    "name": "ownerOf",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1154,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1153,
                                                "name": "tokenId",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1158,
                                                "src": "304:15:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                                "typeName": {
                                                    "id": 1152,
                                                    "name": "uint256",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "304:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_uint256",
                                                        "typeString": "uint256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            }
                                        ],
                                        "src": "303:17:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1157,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1156,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1158,
                                                "src": "337:7:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_address",
                                                    "typeString": "address",
                                                },
                                                "typeName": {
                                                    "id": 1155,
                                                    "name": "address",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "337:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_address",
                                                        "typeString": "address",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            }
                                        ],
                                        "src": "336:9:2",
                                    },
                                    "scope": 1175,
                                    "src": "287:59:2",
                                    "stateMutability": "nonpayable",
                                    "superFunction": None,
                                    "visibility": "public",
                                },
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1167,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": False,
                                    "modifiers": [],
                                    "name": "safeTransferFrom",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1165,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1160,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1167,
                                                "src": "375:7:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_address",
                                                    "typeString": "address",
                                                },
                                                "typeName": {
                                                    "id": 1159,
                                                    "name": "address",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "375:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_address",
                                                        "typeString": "address",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                            {
                                                "constant": False,
                                                "id": 1162,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1167,
                                                "src": "384:7:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_address",
                                                    "typeString": "address",
                                                },
                                                "typeName": {
                                                    "id": 1161,
                                                    "name": "address",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "384:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_address",
                                                        "typeString": "address",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                            {
                                                "constant": False,
                                                "id": 1164,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1167,
                                                "src": "393:7:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                                "typeName": {
                                                    "id": 1163,
                                                    "name": "uint256",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "393:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_uint256",
                                                        "typeString": "uint256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                        ],
                                        "src": "374:27:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1166,
                                        "nodeType": "ParameterList",
                                        "parameters": [],
                                        "src": "408:0:2",
                                    },
                                    "scope": 1175,
                                    "src": "349:60:2",
                                    "stateMutability": "nonpayable",
                                    "superFunction": None,
                                    "visibility": "public",
                                },
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1174,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": False,
                                    "modifiers": [],
                                    "name": "updateOperator",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1170,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1169,
                                                "name": "landId",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1174,
                                                "src": "436:14:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                                "typeName": {
                                                    "id": 1168,
                                                    "name": "uint256",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "436:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_uint256",
                                                        "typeString": "uint256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            }
                                        ],
                                        "src": "435:16:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1173,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1172,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1174,
                                                "src": "468:7:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_address",
                                                    "typeString": "address",
                                                },
                                                "typeName": {
                                                    "id": 1171,
                                                    "name": "address",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "468:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_address",
                                                        "typeString": "address",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            }
                                        ],
                                        "src": "467:9:2",
                                    },
                                    "scope": 1175,
                                    "src": "412:65:2",
                                    "stateMutability": "nonpayable",
                                    "superFunction": None,
                                    "visibility": "public",
                                },
                            ],
                            "scope": 1222,
                            "src": "27:452:2",
                        },
                        {
                            "baseContracts": [],
                            "contractDependencies": [],
                            "contractKind": "contract",
                            "documentation": None,
                            "fullyImplemented": True,
                            "id": 1221,
                            "linearizedBaseContracts": [1221],
                            "name": "EstateStorage",
                            "nodeType": "ContractDefinition",
                            "nodes": [
                                {
                                    "constant": True,
                                    "id": 1182,
                                    "name": "InterfaceId_GetMetadata",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "509:92:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_bytes4",
                                        "typeString": "bytes4",
                                    },
                                    "typeName": {
                                        "id": 1176,
                                        "name": "bytes4",
                                        "nodeType": "ElementaryTypeName",
                                        "src": "509:6:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_bytes4",
                                            "typeString": "bytes4",
                                        },
                                    },
                                    "value": {
                                        "argumentTypes": None,
                                        "arguments": [
                                            {
                                                "argumentTypes": None,
                                                "arguments": [
                                                    {
                                                        "argumentTypes": None,
                                                        "hexValue": "6765744d657461646174612875696e7432353629",
                                                        "id": 1179,
                                                        "isConstant": False,
                                                        "isLValue": False,
                                                        "isPure": True,
                                                        "kind": "string",
                                                        "lValueRequested": False,
                                                        "nodeType": "Literal",
                                                        "src": "577:22:2",
                                                        "subdenomination": None,
                                                        "typeDescriptions": {
                                                            "typeIdentifier": "t_stringliteral_a574cea40cdd0a08ff0bc728ff4c5c786aa5857d851fdb93fd18cd5b4db07388",
                                                            "typeString": 'literal_string "getMetadata(uint256)"',
                                                        },
                                                        "value": "getMetadata(uint256)",
                                                    }
                                                ],
                                                "expression": {
                                                    "argumentTypes": [
                                                        {
                                                            "typeIdentifier": "t_stringliteral_a574cea40cdd0a08ff0bc728ff4c5c786aa5857d851fdb93fd18cd5b4db07388",
                                                            "typeString": 'literal_string "getMetadata(uint256)"',
                                                        }
                                                    ],
                                                    "id": 1178,
                                                    "name": "keccak256",
                                                    "nodeType": "Identifier",
                                                    "overloadedDeclarations": [],
                                                    "referencedDeclaration": 6208,
                                                    "src": "567:9:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_function_sha3_pure$__$returns$_t_bytes32_$",
                                                        "typeString": "function () pure returns (bytes32)",
                                                    },
                                                },
                                                "id": 1180,
                                                "isConstant": False,
                                                "isLValue": False,
                                                "isPure": True,
                                                "kind": "functionCall",
                                                "lValueRequested": False,
                                                "names": [],
                                                "nodeType": "FunctionCall",
                                                "src": "567:33:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_bytes32",
                                                    "typeString": "bytes32",
                                                },
                                            }
                                        ],
                                        "expression": {
                                            "argumentTypes": [
                                                {
                                                    "typeIdentifier": "t_bytes32",
                                                    "typeString": "bytes32",
                                                }
                                            ],
                                            "id": 1177,
                                            "isConstant": False,
                                            "isLValue": False,
                                            "isPure": True,
                                            "lValueRequested": False,
                                            "nodeType": "ElementaryTypeNameExpression",
                                            "src": "560:6:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_type$_t_bytes4_$",
                                                "typeString": "type(bytes4)",
                                            },
                                            "typeName": "bytes4",
                                        },
                                        "id": 1181,
                                        "isConstant": False,
                                        "isLValue": False,
                                        "isPure": True,
                                        "kind": "typeConversion",
                                        "lValueRequested": False,
                                        "names": [],
                                        "nodeType": "FunctionCall",
                                        "src": "560:41:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_bytes4",
                                            "typeString": "bytes4",
                                        },
                                    },
                                    "visibility": "internal",
                                },
                                {
                                    "constant": True,
                                    "id": 1189,
                                    "name": "InterfaceId_VerifyFingerprint",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "605:118:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_bytes4",
                                        "typeString": "bytes4",
                                    },
                                    "typeName": {
                                        "id": 1183,
                                        "name": "bytes4",
                                        "nodeType": "ElementaryTypeName",
                                        "src": "605:6:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_bytes4",
                                            "typeString": "bytes4",
                                        },
                                    },
                                    "value": {
                                        "argumentTypes": None,
                                        "arguments": [
                                            {
                                                "argumentTypes": None,
                                                "arguments": [
                                                    {
                                                        "argumentTypes": None,
                                                        "hexValue": "76657269667946696e6765727072696e742875696e743235362c627974657329",
                                                        "id": 1186,
                                                        "isConstant": False,
                                                        "isLValue": False,
                                                        "isPure": True,
                                                        "kind": "string",
                                                        "lValueRequested": False,
                                                        "nodeType": "Literal",
                                                        "src": "684:34:2",
                                                        "subdenomination": None,
                                                        "typeDescriptions": {
                                                            "typeIdentifier": "t_stringliteral_8f9f4b63fb27ea36c52c6e650320201c8f2c6d7c1dfa95f40f5d5da523920168",
                                                            "typeString": 'literal_string "verifyFingerprint(uint256,bytes)"',
                                                        },
                                                        "value": "verifyFingerprint(uint256,bytes)",
                                                    }
                                                ],
                                                "expression": {
                                                    "argumentTypes": [
                                                        {
                                                            "typeIdentifier": "t_stringliteral_8f9f4b63fb27ea36c52c6e650320201c8f2c6d7c1dfa95f40f5d5da523920168",
                                                            "typeString": 'literal_string "verifyFingerprint(uint256,bytes)"',
                                                        }
                                                    ],
                                                    "id": 1185,
                                                    "name": "keccak256",
                                                    "nodeType": "Identifier",
                                                    "overloadedDeclarations": [],
                                                    "referencedDeclaration": 6208,
                                                    "src": "674:9:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_function_sha3_pure$__$returns$_t_bytes32_$",
                                                        "typeString": "function () pure returns (bytes32)",
                                                    },
                                                },
                                                "id": 1187,
                                                "isConstant": False,
                                                "isLValue": False,
                                                "isPure": True,
                                                "kind": "functionCall",
                                                "lValueRequested": False,
                                                "names": [],
                                                "nodeType": "FunctionCall",
                                                "src": "674:45:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_bytes32",
                                                    "typeString": "bytes32",
                                                },
                                            }
                                        ],
                                        "expression": {
                                            "argumentTypes": [
                                                {
                                                    "typeIdentifier": "t_bytes32",
                                                    "typeString": "bytes32",
                                                }
                                            ],
                                            "id": 1184,
                                            "isConstant": False,
                                            "isLValue": False,
                                            "isPure": True,
                                            "lValueRequested": False,
                                            "nodeType": "ElementaryTypeNameExpression",
                                            "src": "662:6:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_type$_t_bytes4_$",
                                                "typeString": "type(bytes4)",
                                            },
                                            "typeName": "bytes4",
                                        },
                                        "id": 1188,
                                        "isConstant": False,
                                        "isLValue": False,
                                        "isPure": True,
                                        "kind": "typeConversion",
                                        "lValueRequested": False,
                                        "names": [],
                                        "nodeType": "FunctionCall",
                                        "src": "662:61:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_bytes4",
                                            "typeString": "bytes4",
                                        },
                                    },
                                    "visibility": "internal",
                                },
                                {
                                    "constant": False,
                                    "id": 1191,
                                    "name": "registry",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "728:28:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_contract$_LANDRegistry_$1175",
                                        "typeString": "contract LANDRegistry",
                                    },
                                    "typeName": {
                                        "contractScope": None,
                                        "id": 1190,
                                        "name": "LANDRegistry",
                                        "nodeType": "UserDefinedTypeName",
                                        "referencedDeclaration": 1175,
                                        "src": "728:12:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_contract$_LANDRegistry_$1175",
                                            "typeString": "contract LANDRegistry",
                                        },
                                    },
                                    "value": None,
                                    "visibility": "public",
                                },
                                {
                                    "constant": False,
                                    "id": 1196,
                                    "name": "estateLandIds",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "812:50:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_mapping$_t_uint256_$_t_array$_t_uint256_$dyn_storage_$",
                                        "typeString": "mapping(uint256 => uint256[])",
                                    },
                                    "typeName": {
                                        "id": 1195,
                                        "keyType": {
                                            "id": 1192,
                                            "name": "uint256",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "820:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_uint256",
                                                "typeString": "uint256",
                                            },
                                        },
                                        "nodeType": "Mapping",
                                        "src": "812:29:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_mapping$_t_uint256_$_t_array$_t_uint256_$dyn_storage_$",
                                            "typeString": "mapping(uint256 => uint256[])",
                                        },
                                        "valueType": {
                                            "baseType": {
                                                "id": 1193,
                                                "name": "uint256",
                                                "nodeType": "ElementaryTypeName",
                                                "src": "831:7:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                            },
                                            "id": 1194,
                                            "length": None,
                                            "nodeType": "ArrayTypeName",
                                            "src": "831:9:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_array$_t_uint256_$dyn_storage_ptr",
                                                "typeString": "uint256[]",
                                            },
                                        },
                                    },
                                    "value": None,
                                    "visibility": "public",
                                },
                                {
                                    "constant": False,
                                    "id": 1200,
                                    "name": "landIdEstate",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "915:47:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_mapping$_t_uint256_$_t_uint256_$",
                                        "typeString": "mapping(uint256 => uint256)",
                                    },
                                    "typeName": {
                                        "id": 1199,
                                        "keyType": {
                                            "id": 1197,
                                            "name": "uint256",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "923:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_uint256",
                                                "typeString": "uint256",
                                            },
                                        },
                                        "nodeType": "Mapping",
                                        "src": "915:27:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_mapping$_t_uint256_$_t_uint256_$",
                                            "typeString": "mapping(uint256 => uint256)",
                                        },
                                        "valueType": {
                                            "id": 1198,
                                            "name": "uint256",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "934:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_uint256",
                                                "typeString": "uint256",
                                            },
                                        },
                                    },
                                    "value": None,
                                    "visibility": "public",
                                },
                                {
                                    "constant": False,
                                    "id": 1206,
                                    "name": "estateLandIndex",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "1053:70:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_mapping$_t_uint256_$_t_mapping$_t_uint256_$_t_uint256_$_$",
                                        "typeString": "mapping(uint256 => mapping(uint256 => uint256))",
                                    },
                                    "typeName": {
                                        "id": 1205,
                                        "keyType": {
                                            "id": 1201,
                                            "name": "uint256",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "1061:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_uint256",
                                                "typeString": "uint256",
                                            },
                                        },
                                        "nodeType": "Mapping",
                                        "src": "1053:47:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_mapping$_t_uint256_$_t_mapping$_t_uint256_$_t_uint256_$_$",
                                            "typeString": "mapping(uint256 => mapping(uint256 => uint256))",
                                        },
                                        "valueType": {
                                            "id": 1204,
                                            "keyType": {
                                                "id": 1202,
                                                "name": "uint256",
                                                "nodeType": "ElementaryTypeName",
                                                "src": "1080:7:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                            },
                                            "nodeType": "Mapping",
                                            "src": "1072:27:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_mapping$_t_uint256_$_t_uint256_$",
                                                "typeString": "mapping(uint256 => uint256)",
                                            },
                                            "valueType": {
                                                "id": 1203,
                                                "name": "uint256",
                                                "nodeType": "ElementaryTypeName",
                                                "src": "1091:7:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                            },
                                        },
                                    },
                                    "value": None,
                                    "visibility": "public",
                                },
                                {
                                    "constant": False,
                                    "id": 1210,
                                    "name": "estateData",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "1156:46:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_mapping$_t_uint256_$_t_string_storage_$",
                                        "typeString": "mapping(uint256 => string)",
                                    },
                                    "typeName": {
                                        "id": 1209,
                                        "keyType": {
                                            "id": 1207,
                                            "name": "uint256",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "1164:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_uint256",
                                                "typeString": "uint256",
                                            },
                                        },
                                        "nodeType": "Mapping",
                                        "src": "1156:26:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_mapping$_t_uint256_$_t_string_storage_$",
                                            "typeString": "mapping(uint256 => string)",
                                        },
                                        "valueType": {
                                            "id": 1208,
                                            "name": "string",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "1175:6:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_string_storage_ptr",
                                                "typeString": "string",
                                            },
                                        },
                                    },
                                    "value": None,
                                    "visibility": "internal",
                                },
                                {
                                    "constant": False,
                                    "id": 1214,
                                    "name": "updateOperator",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "1235:50:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_mapping$_t_uint256_$_t_address_$",
                                        "typeString": "mapping(uint256 => address)",
                                    },
                                    "typeName": {
                                        "id": 1213,
                                        "keyType": {
                                            "id": 1211,
                                            "name": "uint256",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "1244:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_uint256",
                                                "typeString": "uint256",
                                            },
                                        },
                                        "nodeType": "Mapping",
                                        "src": "1235:28:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_mapping$_t_uint256_$_t_address_$",
                                            "typeString": "mapping(uint256 => address)",
                                        },
                                        "valueType": {
                                            "id": 1212,
                                            "name": "address",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "1255:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_address",
                                                "typeString": "address",
                                            },
                                        },
                                    },
                                    "value": None,
                                    "visibility": "public",
                                },
                                {
                                    "constant": False,
                                    "id": 1220,
                                    "name": "updateManager",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "1383:65:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_mapping$_t_address_$_t_mapping$_t_address_$_t_bool_$_$",
                                        "typeString": "mapping(address => mapping(address => bool))",
                                    },
                                    "typeName": {
                                        "id": 1219,
                                        "keyType": {
                                            "id": 1215,
                                            "name": "address",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "1391:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_address",
                                                "typeString": "address",
                                            },
                                        },
                                        "nodeType": "Mapping",
                                        "src": "1383:44:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_mapping$_t_address_$_t_mapping$_t_address_$_t_bool_$_$",
                                            "typeString": "mapping(address => mapping(address => bool))",
                                        },
                                        "valueType": {
                                            "id": 1218,
                                            "keyType": {
                                                "id": 1216,
                                                "name": "address",
                                                "nodeType": "ElementaryTypeName",
                                                "src": "1410:7:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_address",
                                                    "typeString": "address",
                                                },
                                            },
                                            "nodeType": "Mapping",
                                            "src": "1402:24:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_mapping$_t_address_$_t_bool_$",
                                                "typeString": "mapping(address => bool)",
                                            },
                                            "valueType": {
                                                "id": 1217,
                                                "name": "bool",
                                                "nodeType": "ElementaryTypeName",
                                                "src": "1421:4:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_bool",
                                                    "typeString": "bool",
                                                },
                                            },
                                        },
                                    },
                                    "value": None,
                                    "visibility": "public",
                                },
                            ],
                            "scope": 1222,
                            "src": "482:970:2",
                        },
                    ],
                    "src": "0:1453:2",
                },
                "legacyAST": {
                    "absolutePath": "/home/spoons/diligence/mythx-qa/land/contracts/estate/EstateStorage.sol",
                    "exportedSymbols": {
                        "EstateStorage": [1221],
                        "LANDRegistry": [1175],
                    },
                    "id": 1222,
                    "nodeType": "SourceUnit",
                    "nodes": [
                        {
                            "id": 1123,
                            "literals": ["solidity", "^", "0.4", ".23"],
                            "nodeType": "PragmaDirective",
                            "src": "0:24:2",
                        },
                        {
                            "baseContracts": [],
                            "contractDependencies": [],
                            "contractKind": "contract",
                            "documentation": None,
                            "fullyImplemented": False,
                            "id": 1175,
                            "linearizedBaseContracts": [1175],
                            "name": "LANDRegistry",
                            "nodeType": "ContractDefinition",
                            "nodes": [
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1132,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": True,
                                    "modifiers": [],
                                    "name": "decodeTokenId",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1126,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1125,
                                                "name": "value",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1132,
                                                "src": "76:10:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                                "typeName": {
                                                    "id": 1124,
                                                    "name": "uint",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "76:4:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_uint256",
                                                        "typeString": "uint256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            }
                                        ],
                                        "src": "75:12:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1131,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1128,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1132,
                                                "src": "111:3:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_int256",
                                                    "typeString": "int256",
                                                },
                                                "typeName": {
                                                    "id": 1127,
                                                    "name": "int",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "111:3:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_int256",
                                                        "typeString": "int256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                            {
                                                "constant": False,
                                                "id": 1130,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1132,
                                                "src": "116:3:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_int256",
                                                    "typeString": "int256",
                                                },
                                                "typeName": {
                                                    "id": 1129,
                                                    "name": "int",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "116:3:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_int256",
                                                        "typeString": "int256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                        ],
                                        "src": "110:10:2",
                                    },
                                    "scope": 1175,
                                    "src": "53:68:2",
                                    "stateMutability": "pure",
                                    "superFunction": None,
                                    "visibility": "external",
                                },
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1141,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": False,
                                    "modifiers": [],
                                    "name": "updateLandData",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1139,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1134,
                                                "name": "x",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1141,
                                                "src": "148:5:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_int256",
                                                    "typeString": "int256",
                                                },
                                                "typeName": {
                                                    "id": 1133,
                                                    "name": "int",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "148:3:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_int256",
                                                        "typeString": "int256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                            {
                                                "constant": False,
                                                "id": 1136,
                                                "name": "y",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1141,
                                                "src": "155:5:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_int256",
                                                    "typeString": "int256",
                                                },
                                                "typeName": {
                                                    "id": 1135,
                                                    "name": "int",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "155:3:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_int256",
                                                        "typeString": "int256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                            {
                                                "constant": False,
                                                "id": 1138,
                                                "name": "data",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1141,
                                                "src": "162:11:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_string_calldata_ptr",
                                                    "typeString": "string",
                                                },
                                                "typeName": {
                                                    "id": 1137,
                                                    "name": "string",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "162:6:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_string_storage_ptr",
                                                        "typeString": "string",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                        ],
                                        "src": "147:27:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1140,
                                        "nodeType": "ParameterList",
                                        "parameters": [],
                                        "src": "183:0:2",
                                    },
                                    "scope": 1175,
                                    "src": "124:60:2",
                                    "stateMutability": "nonpayable",
                                    "superFunction": None,
                                    "visibility": "external",
                                },
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1148,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": False,
                                    "modifiers": [],
                                    "name": "setUpdateOperator",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1146,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1143,
                                                "name": "assetId",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1148,
                                                "src": "214:15:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                                "typeName": {
                                                    "id": 1142,
                                                    "name": "uint256",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "214:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_uint256",
                                                        "typeString": "uint256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                            {
                                                "constant": False,
                                                "id": 1145,
                                                "name": "operator",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1148,
                                                "src": "231:16:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_address",
                                                    "typeString": "address",
                                                },
                                                "typeName": {
                                                    "id": 1144,
                                                    "name": "address",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "231:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_address",
                                                        "typeString": "address",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                        ],
                                        "src": "213:35:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1147,
                                        "nodeType": "ParameterList",
                                        "parameters": [],
                                        "src": "257:0:2",
                                    },
                                    "scope": 1175,
                                    "src": "187:71:2",
                                    "stateMutability": "nonpayable",
                                    "superFunction": None,
                                    "visibility": "external",
                                },
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1151,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": False,
                                    "modifiers": [],
                                    "name": "ping",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1149,
                                        "nodeType": "ParameterList",
                                        "parameters": [],
                                        "src": "274:2:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1150,
                                        "nodeType": "ParameterList",
                                        "parameters": [],
                                        "src": "283:0:2",
                                    },
                                    "scope": 1175,
                                    "src": "261:23:2",
                                    "stateMutability": "nonpayable",
                                    "superFunction": None,
                                    "visibility": "public",
                                },
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1158,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": False,
                                    "modifiers": [],
                                    "name": "ownerOf",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1154,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1153,
                                                "name": "tokenId",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1158,
                                                "src": "304:15:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                                "typeName": {
                                                    "id": 1152,
                                                    "name": "uint256",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "304:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_uint256",
                                                        "typeString": "uint256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            }
                                        ],
                                        "src": "303:17:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1157,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1156,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1158,
                                                "src": "337:7:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_address",
                                                    "typeString": "address",
                                                },
                                                "typeName": {
                                                    "id": 1155,
                                                    "name": "address",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "337:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_address",
                                                        "typeString": "address",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            }
                                        ],
                                        "src": "336:9:2",
                                    },
                                    "scope": 1175,
                                    "src": "287:59:2",
                                    "stateMutability": "nonpayable",
                                    "superFunction": None,
                                    "visibility": "public",
                                },
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1167,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": False,
                                    "modifiers": [],
                                    "name": "safeTransferFrom",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1165,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1160,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1167,
                                                "src": "375:7:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_address",
                                                    "typeString": "address",
                                                },
                                                "typeName": {
                                                    "id": 1159,
                                                    "name": "address",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "375:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_address",
                                                        "typeString": "address",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                            {
                                                "constant": False,
                                                "id": 1162,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1167,
                                                "src": "384:7:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_address",
                                                    "typeString": "address",
                                                },
                                                "typeName": {
                                                    "id": 1161,
                                                    "name": "address",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "384:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_address",
                                                        "typeString": "address",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                            {
                                                "constant": False,
                                                "id": 1164,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1167,
                                                "src": "393:7:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                                "typeName": {
                                                    "id": 1163,
                                                    "name": "uint256",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "393:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_uint256",
                                                        "typeString": "uint256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            },
                                        ],
                                        "src": "374:27:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1166,
                                        "nodeType": "ParameterList",
                                        "parameters": [],
                                        "src": "408:0:2",
                                    },
                                    "scope": 1175,
                                    "src": "349:60:2",
                                    "stateMutability": "nonpayable",
                                    "superFunction": None,
                                    "visibility": "public",
                                },
                                {
                                    "body": None,
                                    "documentation": None,
                                    "id": 1174,
                                    "implemented": False,
                                    "isConstructor": False,
                                    "isDeclaredConst": False,
                                    "modifiers": [],
                                    "name": "updateOperator",
                                    "nodeType": "FunctionDefinition",
                                    "parameters": {
                                        "id": 1170,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1169,
                                                "name": "landId",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1174,
                                                "src": "436:14:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                                "typeName": {
                                                    "id": 1168,
                                                    "name": "uint256",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "436:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_uint256",
                                                        "typeString": "uint256",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            }
                                        ],
                                        "src": "435:16:2",
                                    },
                                    "payable": False,
                                    "returnParameters": {
                                        "id": 1173,
                                        "nodeType": "ParameterList",
                                        "parameters": [
                                            {
                                                "constant": False,
                                                "id": 1172,
                                                "name": "",
                                                "nodeType": "VariableDeclaration",
                                                "scope": 1174,
                                                "src": "468:7:2",
                                                "stateVariable": False,
                                                "storageLocation": "default",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_address",
                                                    "typeString": "address",
                                                },
                                                "typeName": {
                                                    "id": 1171,
                                                    "name": "address",
                                                    "nodeType": "ElementaryTypeName",
                                                    "src": "468:7:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_address",
                                                        "typeString": "address",
                                                    },
                                                },
                                                "value": None,
                                                "visibility": "internal",
                                            }
                                        ],
                                        "src": "467:9:2",
                                    },
                                    "scope": 1175,
                                    "src": "412:65:2",
                                    "stateMutability": "nonpayable",
                                    "superFunction": None,
                                    "visibility": "public",
                                },
                            ],
                            "scope": 1222,
                            "src": "27:452:2",
                        },
                        {
                            "baseContracts": [],
                            "contractDependencies": [],
                            "contractKind": "contract",
                            "documentation": None,
                            "fullyImplemented": True,
                            "id": 1221,
                            "linearizedBaseContracts": [1221],
                            "name": "EstateStorage",
                            "nodeType": "ContractDefinition",
                            "nodes": [
                                {
                                    "constant": True,
                                    "id": 1182,
                                    "name": "InterfaceId_GetMetadata",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "509:92:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_bytes4",
                                        "typeString": "bytes4",
                                    },
                                    "typeName": {
                                        "id": 1176,
                                        "name": "bytes4",
                                        "nodeType": "ElementaryTypeName",
                                        "src": "509:6:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_bytes4",
                                            "typeString": "bytes4",
                                        },
                                    },
                                    "value": {
                                        "argumentTypes": None,
                                        "arguments": [
                                            {
                                                "argumentTypes": None,
                                                "arguments": [
                                                    {
                                                        "argumentTypes": None,
                                                        "hexValue": "6765744d657461646174612875696e7432353629",
                                                        "id": 1179,
                                                        "isConstant": False,
                                                        "isLValue": False,
                                                        "isPure": True,
                                                        "kind": "string",
                                                        "lValueRequested": False,
                                                        "nodeType": "Literal",
                                                        "src": "577:22:2",
                                                        "subdenomination": None,
                                                        "typeDescriptions": {
                                                            "typeIdentifier": "t_stringliteral_a574cea40cdd0a08ff0bc728ff4c5c786aa5857d851fdb93fd18cd5b4db07388",
                                                            "typeString": 'literal_string "getMetadata(uint256)"',
                                                        },
                                                        "value": "getMetadata(uint256)",
                                                    }
                                                ],
                                                "expression": {
                                                    "argumentTypes": [
                                                        {
                                                            "typeIdentifier": "t_stringliteral_a574cea40cdd0a08ff0bc728ff4c5c786aa5857d851fdb93fd18cd5b4db07388",
                                                            "typeString": 'literal_string "getMetadata(uint256)"',
                                                        }
                                                    ],
                                                    "id": 1178,
                                                    "name": "keccak256",
                                                    "nodeType": "Identifier",
                                                    "overloadedDeclarations": [],
                                                    "referencedDeclaration": 6208,
                                                    "src": "567:9:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_function_sha3_pure$__$returns$_t_bytes32_$",
                                                        "typeString": "function () pure returns (bytes32)",
                                                    },
                                                },
                                                "id": 1180,
                                                "isConstant": False,
                                                "isLValue": False,
                                                "isPure": True,
                                                "kind": "functionCall",
                                                "lValueRequested": False,
                                                "names": [],
                                                "nodeType": "FunctionCall",
                                                "src": "567:33:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_bytes32",
                                                    "typeString": "bytes32",
                                                },
                                            }
                                        ],
                                        "expression": {
                                            "argumentTypes": [
                                                {
                                                    "typeIdentifier": "t_bytes32",
                                                    "typeString": "bytes32",
                                                }
                                            ],
                                            "id": 1177,
                                            "isConstant": False,
                                            "isLValue": False,
                                            "isPure": True,
                                            "lValueRequested": False,
                                            "nodeType": "ElementaryTypeNameExpression",
                                            "src": "560:6:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_type$_t_bytes4_$",
                                                "typeString": "type(bytes4)",
                                            },
                                            "typeName": "bytes4",
                                        },
                                        "id": 1181,
                                        "isConstant": False,
                                        "isLValue": False,
                                        "isPure": True,
                                        "kind": "typeConversion",
                                        "lValueRequested": False,
                                        "names": [],
                                        "nodeType": "FunctionCall",
                                        "src": "560:41:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_bytes4",
                                            "typeString": "bytes4",
                                        },
                                    },
                                    "visibility": "internal",
                                },
                                {
                                    "constant": True,
                                    "id": 1189,
                                    "name": "InterfaceId_VerifyFingerprint",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "605:118:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_bytes4",
                                        "typeString": "bytes4",
                                    },
                                    "typeName": {
                                        "id": 1183,
                                        "name": "bytes4",
                                        "nodeType": "ElementaryTypeName",
                                        "src": "605:6:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_bytes4",
                                            "typeString": "bytes4",
                                        },
                                    },
                                    "value": {
                                        "argumentTypes": None,
                                        "arguments": [
                                            {
                                                "argumentTypes": None,
                                                "arguments": [
                                                    {
                                                        "argumentTypes": None,
                                                        "hexValue": "76657269667946696e6765727072696e742875696e743235362c627974657329",
                                                        "id": 1186,
                                                        "isConstant": False,
                                                        "isLValue": False,
                                                        "isPure": True,
                                                        "kind": "string",
                                                        "lValueRequested": False,
                                                        "nodeType": "Literal",
                                                        "src": "684:34:2",
                                                        "subdenomination": None,
                                                        "typeDescriptions": {
                                                            "typeIdentifier": "t_stringliteral_8f9f4b63fb27ea36c52c6e650320201c8f2c6d7c1dfa95f40f5d5da523920168",
                                                            "typeString": 'literal_string "verifyFingerprint(uint256,bytes)"',
                                                        },
                                                        "value": "verifyFingerprint(uint256,bytes)",
                                                    }
                                                ],
                                                "expression": {
                                                    "argumentTypes": [
                                                        {
                                                            "typeIdentifier": "t_stringliteral_8f9f4b63fb27ea36c52c6e650320201c8f2c6d7c1dfa95f40f5d5da523920168",
                                                            "typeString": 'literal_string "verifyFingerprint(uint256,bytes)"',
                                                        }
                                                    ],
                                                    "id": 1185,
                                                    "name": "keccak256",
                                                    "nodeType": "Identifier",
                                                    "overloadedDeclarations": [],
                                                    "referencedDeclaration": 6208,
                                                    "src": "674:9:2",
                                                    "typeDescriptions": {
                                                        "typeIdentifier": "t_function_sha3_pure$__$returns$_t_bytes32_$",
                                                        "typeString": "function () pure returns (bytes32)",
                                                    },
                                                },
                                                "id": 1187,
                                                "isConstant": False,
                                                "isLValue": False,
                                                "isPure": True,
                                                "kind": "functionCall",
                                                "lValueRequested": False,
                                                "names": [],
                                                "nodeType": "FunctionCall",
                                                "src": "674:45:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_bytes32",
                                                    "typeString": "bytes32",
                                                },
                                            }
                                        ],
                                        "expression": {
                                            "argumentTypes": [
                                                {
                                                    "typeIdentifier": "t_bytes32",
                                                    "typeString": "bytes32",
                                                }
                                            ],
                                            "id": 1184,
                                            "isConstant": False,
                                            "isLValue": False,
                                            "isPure": True,
                                            "lValueRequested": False,
                                            "nodeType": "ElementaryTypeNameExpression",
                                            "src": "662:6:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_type$_t_bytes4_$",
                                                "typeString": "type(bytes4)",
                                            },
                                            "typeName": "bytes4",
                                        },
                                        "id": 1188,
                                        "isConstant": False,
                                        "isLValue": False,
                                        "isPure": True,
                                        "kind": "typeConversion",
                                        "lValueRequested": False,
                                        "names": [],
                                        "nodeType": "FunctionCall",
                                        "src": "662:61:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_bytes4",
                                            "typeString": "bytes4",
                                        },
                                    },
                                    "visibility": "internal",
                                },
                                {
                                    "constant": False,
                                    "id": 1191,
                                    "name": "registry",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "728:28:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_contract$_LANDRegistry_$1175",
                                        "typeString": "contract LANDRegistry",
                                    },
                                    "typeName": {
                                        "contractScope": None,
                                        "id": 1190,
                                        "name": "LANDRegistry",
                                        "nodeType": "UserDefinedTypeName",
                                        "referencedDeclaration": 1175,
                                        "src": "728:12:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_contract$_LANDRegistry_$1175",
                                            "typeString": "contract LANDRegistry",
                                        },
                                    },
                                    "value": None,
                                    "visibility": "public",
                                },
                                {
                                    "constant": False,
                                    "id": 1196,
                                    "name": "estateLandIds",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "812:50:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_mapping$_t_uint256_$_t_array$_t_uint256_$dyn_storage_$",
                                        "typeString": "mapping(uint256 => uint256[])",
                                    },
                                    "typeName": {
                                        "id": 1195,
                                        "keyType": {
                                            "id": 1192,
                                            "name": "uint256",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "820:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_uint256",
                                                "typeString": "uint256",
                                            },
                                        },
                                        "nodeType": "Mapping",
                                        "src": "812:29:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_mapping$_t_uint256_$_t_array$_t_uint256_$dyn_storage_$",
                                            "typeString": "mapping(uint256 => uint256[])",
                                        },
                                        "valueType": {
                                            "baseType": {
                                                "id": 1193,
                                                "name": "uint256",
                                                "nodeType": "ElementaryTypeName",
                                                "src": "831:7:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                            },
                                            "id": 1194,
                                            "length": None,
                                            "nodeType": "ArrayTypeName",
                                            "src": "831:9:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_array$_t_uint256_$dyn_storage_ptr",
                                                "typeString": "uint256[]",
                                            },
                                        },
                                    },
                                    "value": None,
                                    "visibility": "public",
                                },
                                {
                                    "constant": False,
                                    "id": 1200,
                                    "name": "landIdEstate",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "915:47:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_mapping$_t_uint256_$_t_uint256_$",
                                        "typeString": "mapping(uint256 => uint256)",
                                    },
                                    "typeName": {
                                        "id": 1199,
                                        "keyType": {
                                            "id": 1197,
                                            "name": "uint256",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "923:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_uint256",
                                                "typeString": "uint256",
                                            },
                                        },
                                        "nodeType": "Mapping",
                                        "src": "915:27:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_mapping$_t_uint256_$_t_uint256_$",
                                            "typeString": "mapping(uint256 => uint256)",
                                        },
                                        "valueType": {
                                            "id": 1198,
                                            "name": "uint256",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "934:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_uint256",
                                                "typeString": "uint256",
                                            },
                                        },
                                    },
                                    "value": None,
                                    "visibility": "public",
                                },
                                {
                                    "constant": False,
                                    "id": 1206,
                                    "name": "estateLandIndex",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "1053:70:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_mapping$_t_uint256_$_t_mapping$_t_uint256_$_t_uint256_$_$",
                                        "typeString": "mapping(uint256 => mapping(uint256 => uint256))",
                                    },
                                    "typeName": {
                                        "id": 1205,
                                        "keyType": {
                                            "id": 1201,
                                            "name": "uint256",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "1061:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_uint256",
                                                "typeString": "uint256",
                                            },
                                        },
                                        "nodeType": "Mapping",
                                        "src": "1053:47:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_mapping$_t_uint256_$_t_mapping$_t_uint256_$_t_uint256_$_$",
                                            "typeString": "mapping(uint256 => mapping(uint256 => uint256))",
                                        },
                                        "valueType": {
                                            "id": 1204,
                                            "keyType": {
                                                "id": 1202,
                                                "name": "uint256",
                                                "nodeType": "ElementaryTypeName",
                                                "src": "1080:7:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                            },
                                            "nodeType": "Mapping",
                                            "src": "1072:27:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_mapping$_t_uint256_$_t_uint256_$",
                                                "typeString": "mapping(uint256 => uint256)",
                                            },
                                            "valueType": {
                                                "id": 1203,
                                                "name": "uint256",
                                                "nodeType": "ElementaryTypeName",
                                                "src": "1091:7:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_uint256",
                                                    "typeString": "uint256",
                                                },
                                            },
                                        },
                                    },
                                    "value": None,
                                    "visibility": "public",
                                },
                                {
                                    "constant": False,
                                    "id": 1210,
                                    "name": "estateData",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "1156:46:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_mapping$_t_uint256_$_t_string_storage_$",
                                        "typeString": "mapping(uint256 => string)",
                                    },
                                    "typeName": {
                                        "id": 1209,
                                        "keyType": {
                                            "id": 1207,
                                            "name": "uint256",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "1164:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_uint256",
                                                "typeString": "uint256",
                                            },
                                        },
                                        "nodeType": "Mapping",
                                        "src": "1156:26:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_mapping$_t_uint256_$_t_string_storage_$",
                                            "typeString": "mapping(uint256 => string)",
                                        },
                                        "valueType": {
                                            "id": 1208,
                                            "name": "string",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "1175:6:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_string_storage_ptr",
                                                "typeString": "string",
                                            },
                                        },
                                    },
                                    "value": None,
                                    "visibility": "internal",
                                },
                                {
                                    "constant": False,
                                    "id": 1214,
                                    "name": "updateOperator",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "1235:50:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_mapping$_t_uint256_$_t_address_$",
                                        "typeString": "mapping(uint256 => address)",
                                    },
                                    "typeName": {
                                        "id": 1213,
                                        "keyType": {
                                            "id": 1211,
                                            "name": "uint256",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "1244:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_uint256",
                                                "typeString": "uint256",
                                            },
                                        },
                                        "nodeType": "Mapping",
                                        "src": "1235:28:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_mapping$_t_uint256_$_t_address_$",
                                            "typeString": "mapping(uint256 => address)",
                                        },
                                        "valueType": {
                                            "id": 1212,
                                            "name": "address",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "1255:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_address",
                                                "typeString": "address",
                                            },
                                        },
                                    },
                                    "value": None,
                                    "visibility": "public",
                                },
                                {
                                    "constant": False,
                                    "id": 1220,
                                    "name": "updateManager",
                                    "nodeType": "VariableDeclaration",
                                    "scope": 1221,
                                    "src": "1383:65:2",
                                    "stateVariable": True,
                                    "storageLocation": "default",
                                    "typeDescriptions": {
                                        "typeIdentifier": "t_mapping$_t_address_$_t_mapping$_t_address_$_t_bool_$_$",
                                        "typeString": "mapping(address => mapping(address => bool))",
                                    },
                                    "typeName": {
                                        "id": 1219,
                                        "keyType": {
                                            "id": 1215,
                                            "name": "address",
                                            "nodeType": "ElementaryTypeName",
                                            "src": "1391:7:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_address",
                                                "typeString": "address",
                                            },
                                        },
                                        "nodeType": "Mapping",
                                        "src": "1383:44:2",
                                        "typeDescriptions": {
                                            "typeIdentifier": "t_mapping$_t_address_$_t_mapping$_t_address_$_t_bool_$_$",
                                            "typeString": "mapping(address => mapping(address => bool))",
                                        },
                                        "valueType": {
                                            "id": 1218,
                                            "keyType": {
                                                "id": 1216,
                                                "name": "address",
                                                "nodeType": "ElementaryTypeName",
                                                "src": "1410:7:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_address",
                                                    "typeString": "address",
                                                },
                                            },
                                            "nodeType": "Mapping",
                                            "src": "1402:24:2",
                                            "typeDescriptions": {
                                                "typeIdentifier": "t_mapping$_t_address_$_t_bool_$",
                                                "typeString": "mapping(address => bool)",
                                            },
                                            "valueType": {
                                                "id": 1217,
                                                "name": "bool",
                                                "nodeType": "ElementaryTypeName",
                                                "src": "1421:4:2",
                                                "typeDescriptions": {
                                                    "typeIdentifier": "t_bool",
                                                    "typeString": "bool",
                                                },
                                            },
                                        },
                                    },
                                    "value": None,
                                    "visibility": "public",
                                },
                            ],
                            "scope": 1222,
                            "src": "482:970:2",
                        },
                    ],
                    "src": "0:1453:2",
                },
            }
        },
        "sourceList": [
            "/home/spoons/diligence/mythx-qa/land/contracts/estate/EstateStorage.sol"
        ],
        "version": "0.4.24+commit.e67f0147.Emscripten.clang",
        "analysisMode": "quick",
    }
)
ISSUES_RESPONSE_SIMPLE = """UUID: ab9092f7-54d0-480f-9b63-1bb1508280e2
Title: Assert Violation (Low)
Description: It is possible to trigger an exception (opcode 0xfe). Exceptions can be caused by type errors, division by zero, out-of-bounds array access, or assert violations. Note that explicit `assert()` should only be used to check invariants. Use `require()` for regular input checking.


/home/spoons/diligence/mythx-qa/land/contracts/estate/EstateStorage.sol:24
  mapping(uint256 => uint256[]) public estateLandIds;

UUID: ab9092f7-54d0-480f-9b63-1bb1508280e2
Title: - (Low)
Description: Warning: Free mode only detects certain types of smart contract vulnerabilities. Your contract may still be unsafe. Upgrade to MythX Pro to unlock the ability to test for even more vulnerabilities, perform deeper security analysis, and more. https://mythx.io/plans

"""

ISSUES_RESPONSE_TABLE = """Warning: Free mode only detects certain types of smart contract vulnerabilities. Your contract may still be unsafe. Upgrade to MythX Pro to unlock the ability to test for even more vulnerabilities, perform deeper security analysis, and more. https://mythx.io/plans

Report for /home/spoons/diligence/mythx-qa/land/contracts/estate/EstateStorage.sol
╒════════╤══════════════════╤════════════╤══════════════════════════════════════════╕
│   Line │ SWC Title        │ Severity   │ Short Description                        │
╞════════╪══════════════════╪════════════╪══════════════════════════════════════════╡
│     24 │ Assert Violation │ Low        │ A reachable exception has been detected. │
╘════════╧══════════════════╧════════════╧══════════════════════════════════════════╛
"""
