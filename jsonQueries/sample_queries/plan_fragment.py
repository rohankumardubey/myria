#!/usr/bin/env python

import json

def pretty_json(obj):
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))

def scan_then_insert():
    query_scan = {
        'op_type' : 'SQLiteScan',
        'op_name' : 'Scan',
        'relation_key' : {
            'user_name' : 'jwang',
            'program_name' : 'global_join',
            'relation_name' : 'smallTable'
        },
    }

    insert = {
        'op_type' : 'SQLiteInsert',
        'op_name' : 'Insert',
        'arg_child' : 'Scan',
        'arg_overwrite_table' : True,
        'relation_key' : {
            'user_name' : 'jwang',
            'program_name' : 'global_join',
            'relation_name' : 'smallTable2'
        }
    }

    fragment = {
       'workers' : [1, 2],
       'operators' : [query_scan, insert]
    }
    whole_plan = {
       'raw_datalog' : 'smallTable2(_) :- smallTable(_).',
       'logical_ra' : 'Insert[Scan[smallTable], smallTable2]',
       'fragments' : [fragment]
    }
    return whole_plan

def repartition_on_x():
    query_scan = {
        'op_type' : 'SQLiteScan',
        'op_name' : 'Scan',
        'relation_key' : {
            'user_name' : 'jwang',
            'program_name' : 'global_join',
            'relation_name' : 'smallTable'
        },
    }
    scatter = {
        'op_type' : 'ShuffleProducer',
        'op_name' : 'Scatter',
        'arg_child' : 'Scan',
        'arg_operator_id' : 'hash(follower)',
        'arg_pf' : {
            'type' : 'SingleFieldHash',
            'index' : 0
        }
    }
    gather = {
        'op_type' : 'ShuffleConsumer',
        'op_name' : 'Gather',
        'arg_operator_id' : 'hash(follower)',
        "arg_schema" : {
            "column_types" : ["LONG_TYPE", "LONG_TYPE"],
            "column_names" : ["follower", "followee"]
        }
    }
    insert = {
        'op_type' : 'SQLiteInsert',
        'op_name' : 'Insert',
        'arg_child' : 'Gather',
        'arg_overwrite_table' : True,
        'relation_key' : {
            'user_name' : 'jwang',
            'program_name' : 'global_join',
            'relation_name' : 'smallTable_hash_follower'
        }
    }

    fragment1 = {
       'operators' : [query_scan, scatter]
    }
    fragment2 = {
       'operators' : [gather, insert]
    }
    whole_plan = {
       'raw_datalog' : 'smallTable_hash_follower(x,y) :- smallTable(x,y), @hash(x).',
       'logical_ra' : 'Insert[Shuffle(0)[Scan[smallTable], smallTable2]]',
       'fragments' : [fragment1, fragment2]
    }
    return whole_plan

def single_join():
    scan0 = {
        'op_type' : 'SQLiteScan',
        'op_name' : 'Scan0',
        'relation_key' : {
            'user_name' : 'jwang',
            'program_name' : 'global_join',
            'relation_name' : 'smallTable'
        },
    }
    scatter0 = {
        'op_type' : 'ShuffleProducer',
        'op_name' : 'Scatter0',
        'arg_child' : 'Scan0',
        'arg_operator_id' : 'hash(x)',
        'arg_pf' : {
            'type' : 'SingleFieldHash',
            'index' : 0
        }
    }
    gather0 = {
        'op_type' : 'ShuffleConsumer',
        'op_name' : 'Gather0',
        'arg_operator_id' : 'hash(x)',
        "arg_schema" : {
            "column_types" : ["LONG_TYPE", "LONG_TYPE"],
            "column_names" : ["follower", "followee"]
        }
    }

    scan1 = {
        'op_type' : 'SQLiteScan',
        'op_name' : 'Scan1',
        'relation_key' : {
            'user_name' : 'jwang',
            'program_name' : 'global_join',
            'relation_name' : 'smallTable'
        },
    }
    scatter1 = {
        'op_type' : 'ShuffleProducer',
        'op_name' : 'Scatter1',
        'arg_child' : 'Scan1',
        'arg_operator_id' : 'hash(y)',
        'arg_pf' : {
            'type' : 'SingleFieldHash',
            'index' : 1
        }
    }
    gather1 = {
        'op_type' : 'ShuffleConsumer',
        'op_name' : 'Gather1',
        'arg_operator_id' : 'hash(y)',
        "arg_schema" : {
            "column_types" : ["LONG_TYPE", "LONG_TYPE"],
            "column_names" : ["follower", "followee"]
        }
    }

    join = {
        'op_type' : 'LocalJoin',
        'op_name' : 'Join',
        'arg_child1' : 'Gather1',
        'arg_child2' : 'Gather0',
        'arg_columns1' : [1],
        'arg_columns2' : [0],
        'arg_select1' : [0],
        'arg_select2' : [1],
    }
    insert = {
        'op_type' : 'SQLiteInsert',
        'op_name' : 'Insert',
        'arg_child' : 'Join',
        'arg_overwrite_table' : True,
        'relation_key' : {
            'user_name' : 'jwang',
            'program_name' : 'global_join',
            'relation_name' : 'smallTable_join_smallTable'
        }
    }

    fragmentLeft = {
        'operators' : [scan0, scatter0],
        'workers' : [1, 2]
    }
    fragmentRight = {
        'operators' : [scan1, scatter1],
        'workers' : [1, 2]
    }
    fragmentJoin = {
        'operators' : [gather0, gather1, join, insert],
        'workers' : [3, 4]
    }
    whole_plan = {
       'raw_datalog' : 'smallTable_join_smallTable(x,z) :- smallTable(x,y), mallTable(y,z)',
       'logical_ra' : 'Insert(smallTable_join_smallTable)[Join(1=0; [0,3])[Shuffle(1)[Scan], Shuffle(1)[Scan]]]',
       'fragments' : [fragmentLeft, fragmentRight, fragmentJoin]
    }
    return whole_plan

#print pretty_json(repartition_on_x())
print pretty_json(single_join())
