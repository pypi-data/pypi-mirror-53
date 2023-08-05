# -*- coding: utf-8 -*-
DESC = "tbaas-2018-04-16"
INFO = {
  "Invoke": {
    "params": [
      {
        "name": "Module",
        "desc": "模块名，固定字段：transaction"
      },
      {
        "name": "Operation",
        "desc": "操作名，固定字段：invoke"
      },
      {
        "name": "ClusterId",
        "desc": "区块链网络ID，可在区块链网络详情或列表中获取"
      },
      {
        "name": "ChaincodeName",
        "desc": "业务所属智能合约名称，可在智能合约详情或列表中获取"
      },
      {
        "name": "ChannelName",
        "desc": "业务所属通道名称，可在通道详情或列表中获取"
      },
      {
        "name": "Peers",
        "desc": "对该笔交易进行背书的节点列表（包括节点名称和节点所属组织名称，详见数据结构一节），可以在通道详情中获取该通道上的节点名称极其所属组织名称"
      },
      {
        "name": "FuncName",
        "desc": "该笔交易需要调用的智能合约中的函数名称"
      },
      {
        "name": "GroupName",
        "desc": "调用合约的组织名称，可以在组织管理列表中获取当前组织的名称"
      },
      {
        "name": "Args",
        "desc": "被调用的函数参数列表"
      },
      {
        "name": "AsyncFlag",
        "desc": "同步调用标识，可选参数，值为0或者不传表示使用同步方法调用，调用后会等待交易执行后再返回执行结果；值为1时表示使用异步方式调用Invoke，执行后会立即返回交易对应的Txid，后续需要通过GetInvokeTx这个API查询该交易的执行结果。（对于逻辑较为简单的交易，可以使用同步模式；对于逻辑较为复杂的交易，建议使用异步模式，否则容易导致API因等待时间过长，返回等待超时）"
      }
    ],
    "desc": "新增交易"
  },
  "GetClusterSummary": {
    "params": [
      {
        "name": "Module",
        "desc": "模块名称，固定字段：cluster_mng"
      },
      {
        "name": "Operation",
        "desc": "操作名称，固定字段：cluster_summary"
      },
      {
        "name": "ClusterId",
        "desc": "区块链网络ID，可在区块链网络详情或列表中获取"
      },
      {
        "name": "GroupId",
        "desc": "组织ID，固定字段：0"
      },
      {
        "name": "GroupName",
        "desc": "调用接口的组织名称，可以在组织管理列表中获取当前组织的名称"
      }
    ],
    "desc": "获取区块链网络概要"
  },
  "GetInvokeTx": {
    "params": [
      {
        "name": "Module",
        "desc": "模块名，固定字段：transaction"
      },
      {
        "name": "Operation",
        "desc": "操作名，固定字段：query_txid"
      },
      {
        "name": "ClusterId",
        "desc": "区块链网络ID，可在区块链网络详情或列表中获取"
      },
      {
        "name": "ChannelName",
        "desc": "业务所属通道名称，可在通道详情或列表中获取"
      },
      {
        "name": "PeerName",
        "desc": "执行该查询交易的节点名称，可以在通道详情中获取该通道上的节点名称极其所属组织名称"
      },
      {
        "name": "PeerGroup",
        "desc": "执行该查询交易的节点所属组织名称，可以在通道详情中获取该通道上的节点名称极其所属组织名称"
      },
      {
        "name": "TxId",
        "desc": "交易ID"
      },
      {
        "name": "GroupName",
        "desc": "调用合约的组织名称，可以在组织管理列表中获取当前组织的名称"
      }
    ],
    "desc": "Invoke异步调用结果查询"
  },
  "GetBlockList": {
    "params": [
      {
        "name": "Module",
        "desc": "模块名称，固定字段：block"
      },
      {
        "name": "Operation",
        "desc": "操作名称，固定字段：block_list"
      },
      {
        "name": "ChannelId",
        "desc": "通道ID，固定字段：0"
      },
      {
        "name": "GroupId",
        "desc": "组织ID，固定字段：0"
      },
      {
        "name": "ChannelName",
        "desc": "需要查询的通道名称，可在通道详情或列表中获取"
      },
      {
        "name": "GroupName",
        "desc": "调用接口的组织名称，可以在组织管理列表中获取当前组织的名称"
      },
      {
        "name": "ClusterId",
        "desc": "区块链网络ID，可在区块链网络详情或列表中获取"
      },
      {
        "name": "Offset",
        "desc": "需要获取的起始交易偏移"
      },
      {
        "name": "Limit",
        "desc": "需要获取的交易数量"
      }
    ],
    "desc": "查看当前网络下的所有区块列表，分页展示"
  },
  "Query": {
    "params": [
      {
        "name": "Module",
        "desc": "模块名，固定字段：transaction"
      },
      {
        "name": "Operation",
        "desc": "操作名，固定字段：query"
      },
      {
        "name": "ClusterId",
        "desc": "区块链网络ID，可在区块链网络详情或列表中获取"
      },
      {
        "name": "ChaincodeName",
        "desc": "业务所属智能合约名称，可在智能合约详情或列表中获取"
      },
      {
        "name": "ChannelName",
        "desc": "业务所属通道名称，可在通道详情或列表中获取"
      },
      {
        "name": "Peers",
        "desc": "执行该查询交易的节点列表（包括节点名称和节点所属组织名称，详见数据结构一节），可以在通道详情中获取该通道上的节点名称极其所属组织名称"
      },
      {
        "name": "FuncName",
        "desc": "该笔交易查询需要调用的智能合约中的函数名称"
      },
      {
        "name": "GroupName",
        "desc": "调用合约的组织名称，可以在组织管理列表中获取当前组织的名称"
      },
      {
        "name": "Args",
        "desc": "被调用的函数参数列表"
      }
    ],
    "desc": "查询交易"
  },
  "GetLatesdTransactionList": {
    "params": [
      {
        "name": "Module",
        "desc": "模块名称，固定字段：transaction"
      },
      {
        "name": "Operation",
        "desc": "操作名称，固定字段：latest_transaction_list"
      },
      {
        "name": "GroupId",
        "desc": "组织ID，固定字段：0"
      },
      {
        "name": "ChannelId",
        "desc": "通道ID，固定字段：0"
      },
      {
        "name": "LatestBlockNumber",
        "desc": "获取的最新交易的区块数量，取值范围1~5"
      },
      {
        "name": "GroupName",
        "desc": "调用接口的组织名称，可以在组织管理列表中获取当前组织的名称"
      },
      {
        "name": "ChannelName",
        "desc": "需要查询的通道名称，可在通道详情或列表中获取"
      },
      {
        "name": "ClusterId",
        "desc": "区块链网络ID，可在区块链网络详情或列表中获取"
      },
      {
        "name": "Offset",
        "desc": "需要获取的起始交易偏移"
      },
      {
        "name": "Limit",
        "desc": "需要获取的交易数量"
      }
    ],
    "desc": "获取最新交易列表"
  }
}