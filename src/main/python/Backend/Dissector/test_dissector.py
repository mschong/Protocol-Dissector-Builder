import pytest
from dissector import Dissector_Generator

test_json = {
    "name": "mongodb",
    "created": "12/02/2019 16:39:56",
    "edited": "12/02/2019 16:39:56",
    "description": "mongodb Protocol",
    "protocol": "tcp",
    "change_protocol": "mongodb",
    "src_port": "27017",
    "dst_port": "-1",
    "author": "Daniel O",
    "dissector": {
        "START": "CodeBlock0",
        "CodeBlock0": {
            "Code": "length = buffer:len()",
            "Position": {
                "x": 300.0,
                "y": 228.0
            },
            "Type": "CodeBlock",
            "next_field": "Decision0"
        },
        "Decision0": {
            "Condition": {
                "operand1": "length",
                "operator1": "==",
                "operand2": "0"
            },
            "Position": {
                "x": 301.0,
                "y": 301.0
            },
            "true": "CodeBlock1",
            "false": "message_length",
            "Type": "Decision"
        },
        "CodeBlock1": {
            "Code": "return",
            "Position": {
                "x": 623.0,
                "y": 373.0
            },
            "Type": "CodeBlock",
            "next_field": "END"
        },
        "message_length": {
            "Name": "message_length",
            "Abbreviation": "message_length",
            "Description": "messageLength",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 259.0,
                "y": 373.0
            },
            "Type": "Field",
            "next_field": "request_id"
        },
        "request_id": {
            "Name": "request_id",
            "Abbreviation": "request_id",
            "Description": "RequestID",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 260.0,
                "y": 438.0
            },
            "Type": "Field",
            "next_field": "response_to"
        },
        "response_to": {
            "Name": "response_to",
            "Abbreviation": "response_to",
            "Description": "responseTo",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 260.0,
                "y": 503.0
            },
            "Type": "Field",
            "next_field": "CodeBlock3"
        },
        "CodeBlock3": {
            "Code": " local opcode_number = buffer(12,4):le_uint()\n    local opcode_name = get_opcode_name(opcode_number)",
            "Position": {
                "x": 261.0,
                "y": 566.0
            },
            "Type": "CodeBlock",
            "next_field": "opcode"
        },
        "opcode": {
            "Name": "opcode",
            "Abbreviation": "opcode",
            "Description": "opCode",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 261.0,
                "y": 622.0
            },
            "Type": "Field",
            "next_field": "Decision1"
        },
        "Decision1": {
            "Condition": {
                "operand1": "opcode_name",
                "operator1": "==",
                "operand2": "\"OP_QUERY\""
            },
            "Position": {
                "x": 261.0,
                "y": 702.0
            },
            "true": "CodeBlock4",
            "false": "Decision3",
            "Type": "Decision"
        },
        "CodeBlock4": {
            "Code": "local flags_number = buffer(16,4):le_uint()\n        local flags_description = get_flag_description(flags_number)",
            "Position": {
                "x": 632.0,
                "y": 756.0
            },
            "Type": "CodeBlock",
            "next_field": "flags"
        },
        "flags": {
            "Name": "flags",
            "Abbreviation": "flags",
            "Description": "flags",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 663.0,
                "y": 855.125
            },
            "Type": "Field",
            "next_field": "CodeBlock5"
        },
        "CodeBlock5": {
            "Code": "local string_length",
            "Position": {
                "x": 673.0,
                "y": 953.3125
            },
            "Type": "CodeBlock",
            "next_field": "ForLoop0"
        },
        "ForLoop0": {
            "Expressions": {
                "exp1": "i=20",
                "exp2": "length-1",
                "exp3": "1"
            },
            "Position": {
                "x": 603.75,
                "y": 1032.0
            },
            "true": "Decision2",
            "false": "full_coll_name",
            "Type": "for"
        },
        "Decision2": {
            "Condition": {
                "operand1": "buffer(i,1):le_uint()",
                "operator1": "==",
                "operand2": "0"
            },
            "Position": {
                "x": 963.0,
                "y": 1056.4375
            },
            "true": "CodeBlock6",
            "false": "End_ForLoop0",
            "Type": "Decision"
        },
        "CodeBlock6": {
            "Code": "  string_length = i - 20\n                break",
            "Position": {
                "x": 1115.0,
                "y": 1147.0
            },
            "Type": "CodeBlock",
            "next_field": "END"
        },
        "End_ForLoop0": {
            "Position": {
                "x": 797.4375,
                "y": 1145.5625
            },
            "Type": "End Loop",
            "next_field": "ForLoop0"
        },
        "full_coll_name": {
            "Name": "full_coll_name",
            "Abbreviation": "full_coll_name",
            "Description": "fullCollectionName",
            "Data Type": "STRING",
            "Base": "ASCII",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 532.0,
                "y": 1103.0
            },
            "Type": "Field",
            "next_field": "number_to_skip"
        },
        "number_to_skip": {
            "Name": "number_to_skip",
            "Abbreviation": "number_to_skip",
            "Description": "numberToSkip",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 533.0,
                "y": 1192.0
            },
            "Type": "Field",
            "next_field": "number_to_return"
        },
        "number_to_return": {
            "Name": "number_to_return",
            "Abbreviation": "number_to_return",
            "Description": "numberToReturn",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 478.0,
                "y": 1244.0
            },
            "Type": "Field",
            "next_field": "query"
        },
        "query": {
            "Name": "query",
            "Abbreviation": "query",
            "Description": "query",
            "Data Type": "NONE",
            "Base": "HEX",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "1",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 782.0,
                "y": 1249.0
            },
            "Type": "Field",
            "next_field": "END"
        },
        "Decision3": {
            "Condition": {
                "operand1": "opcode_name",
                "operator1": "==",
                "operand2": "\"OP_REPLY\""
            },
            "Position": {
                "x": 196.0,
                "y": 794.0
            },
            "true": "response_flags",
            "false": "END",
            "Type": "Decision"
        },
        "response_flags": {
            "Name": "response_flags",
            "Abbreviation": "response_flags",
            "Description": "responseFlags",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 297.0,
                "y": 931.0
            },
            "Type": "Field",
            "next_field": "cursor_id"
        },
        "cursor_id": {
            "Name": "cursor_id",
            "Abbreviation": "cursor_id",
            "Description": "cursorId",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "8",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 297.0,
                "y": 990.0
            },
            "Type": "Field",
            "next_field": "starting_from"
        },
        "starting_from": {
            "Name": "starting_from",
            "Abbreviation": "starting_from",
            "Description": "startingFrom",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 257.0,
                "y": 1054.0
            },
            "Type": "Field",
            "next_field": "number_returned"
        },
        "number_returned": {
            "Name": "number_returned",
            "Abbreviation": "number_returned",
            "Description": "numberReturned",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 232.0,
                "y": 1116.0
            },
            "Type": "Field",
            "next_field": "document"
        },
        "document": {
            "Name": "document",
            "Abbreviation": "document",
            "Description": "document",
            "Data Type": "NONE",
            "Base": "HEX",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "1",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 221.0,
                "y": 1184.0
            },
            "Type": "Field",
            "next_field": "END"
        }
    },
    "path": "/Users/danielornelas/projects/protocol-dissector-builder/Protocol-Dissector-Builder/SAMPLE/MongoDB.pdbproj"
}

test_json2 = {}

test_json3 = {
    "name": "mongodb",
    "created": "12/02/2019 16:39:56",
    "edited": "12/02/2019 16:39:56",
    "description": "mongodb Protocol",
    "protocol": "tcp",
    "change_protocol": "mongodb",
    "src_port": "27017",
    "dst_port": "-1",
    "author": "Daniel O",
    "dissector": {
        "START": "CodeBlock0",
        "CodeBlock0": {
            "Code": "length = buffer:len()",
            "Position": {
                "x": 300.0,
                "y": 228.0
            },
            "Type": "CodeBlock",
            "next_field": "Decision0"
        },
        "Decision0": {
            "Condition": {
                "operand1": "length",
                "operator1": "==",
                "operand2": "0"
            },
            "Position": {
                "x": 301.0,
                "y": 301.0
            },
            "true": "CodeBlock1",
            "false": "message_length",
            "Type": "Decision"
        },
        "CodeBlock1": {
            "Code": "return",
            "Position": {
                "x": 623.0,
                "y": 373.0
            },
            "Type": "CodeBlock",
            "next_field": "END"
        },
        "message_length": {
            "Name": "message_length",
            "Abbreviation": "message_length",
            "Description": "messageLength",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 259.0,
                "y": 373.0
            },
            "Type": "Field",
            "next_field": "request_id"
        },
        "request_id": {
            "Name": "request_id",
            "Abbreviation": "request_id",
            "Description": "RequestID",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 260.0,
                "y": 438.0
            },
            "Type": "Field",
            "next_field": "response_to"
        },
        "response_to": {
            "Name": "response_to",
            "Abbreviation": "response_to",
            "Description": "responseTo",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 260.0,
                "y": 503.0
            },
            "Type": "Field",
            "next_field": "CodeBlock3"
        },
        "CodeBlock3": {
            "Code": " local opcode_number = buffer(12,4):le_uint()\n    local opcode_name = get_opcode_name(opcode_number)",
            "Position": {
                "x": 261.0,
                "y": 566.0
            },
            "Type": "CodeBlock",
            "next_field": "opcode"
        },
        "opcode": {
            "Name": "opcode",
            "Abbreviation": "opcode",
            "Description": "opCode",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 261.0,
                "y": 622.0
            },
            "Type": "Field",
            "next_field": "Decision1"
        },
        "Decision1": {
            "Condition": {
                "operand1": "opcode_name",
                "operator1": "==",
                "operand2": "\"OP_QUERY\""
            },
            "Position": {
                "x": 261.0,
                "y": 702.0
            },
            "true": "CodeBlock4",
            "false": "Decision3",
            "Type": "Decision"
        },
        "CodeBlock4": {
            "Code": "local flags_number = buffer(16,4):le_uint()\n        local flags_description = get_flag_description(flags_number)",
            "Position": {
                "x": 632.0,
                "y": 756.0
            },
            "Type": "CodeBlock",
            "next_field": "flags"
        },
        "flags": {
            "Name": "flags",
            "Abbreviation": "flags",
            "Description": "flags",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 663.0,
                "y": 855.125
            },
            "Type": "Field",
            "next_field": "CodeBlock5"
        },
        "CodeBlock5": {
            "Code": "local string_length",
            "Position": {
                "x": 673.0,
                "y": 953.3125
            },
            "Type": "CodeBlock",
            "next_field": "ForLoop0"
        },
        "ForLoop0": {
            "Expressions": {
                "exp1": "i=20",
                "exp2": "length-1",
                "exp3": "1"
            },
            "Position": {
                "x": 603.75,
                "y": 1032.0
            },
            "true": "Decision2",
            "false": "full_coll_name",
            "Type": "for"
        },
        "Decision2": {
            "Condition": {
                "operand1": "buffer(i,1):le_uint()",
                "operator1": "==",
                "operand2": "0"
            },
            "Position": {
                "x": 963.0,
                "y": 1056.4375
            },
            "true": "CodeBlock6",
            "false": "End_ForLoop0",
            "Type": "Decision"
        },
        "CodeBlock6": {
            "Code": "  string_length = i - 20\n                break",
            "Position": {
                "x": 1115.0,
                "y": 1147.0
            },
            "Type": "CodeBlock",
            "next_field": "END"
        },
        "End_ForLoop0": {
            "Position": {
                "x": 797.4375,
                "y": 1145.5625
            },
            "Type": "End Loop",
            "next_field": "ForLoop0"
        },
        "full_coll_name": {
            "Name": "full_coll_name",
            "Abbreviation": "full_coll_name",
            "Description": "fullCollectionName",
            "Data Type": "STRING",
            "Base": "ASCII",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "message_length",
                "combobox": "Field"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 532.0,
                "y": 1103.0
            },
            "Type": "Field",
            "next_field": "number_to_skip"
        },
        "number_to_skip": {
            "Name": "number_to_skip",
            "Abbreviation": "number_to_skip",
            "Description": "numberToSkip",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 533.0,
                "y": 1192.0
            },
            "Type": "Field",
            "next_field": "number_to_return"
        },
        "number_to_return": {
            "Name": "number_to_return",
            "Abbreviation": "number_to_return",
            "Description": "numberToReturn",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 478.0,
                "y": 1244.0
            },
            "Type": "Field",
            "next_field": "query"
        },
        "query": {
            "Name": "query",
            "Abbreviation": "query",
            "Description": "query",
            "Data Type": "NONE",
            "Base": "HEX",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "1",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 782.0,
                "y": 1249.0
            },
            "Type": "Field",
            "next_field": "END"
        },
        "Decision3": {
            "Condition": {
                "operand1": "opcode_name",
                "operator1": "==",
                "operand2": "\"OP_REPLY\""
            },
            "Position": {
                "x": 196.0,
                "y": 794.0
            },
            "true": "response_flags",
            "false": "END",
            "Type": "Decision"
        },
        "response_flags": {
            "Name": "response_flags",
            "Abbreviation": "response_flags",
            "Description": "responseFlags",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 297.0,
                "y": 931.0
            },
            "Type": "Field",
            "next_field": "cursor_id"
        },
        "cursor_id": {
            "Name": "cursor_id",
            "Abbreviation": "cursor_id",
            "Description": "cursorId",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "8",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 297.0,
                "y": 990.0
            },
            "Type": "Field",
            "next_field": "starting_from"
        },
        "starting_from": {
            "Name": "starting_from",
            "Abbreviation": "starting_from",
            "Description": "startingFrom",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 257.0,
                "y": 1054.0
            },
            "Type": "Field",
            "next_field": "number_returned"
        },
        "number_returned": {
            "Name": "number_returned",
            "Abbreviation": "number_returned",
            "Description": "numberReturned",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 232.0,
                "y": 1116.0
            },
            "Type": "Field",
            "next_field": "document"
        },
        "document": {
            "Name": "document",
            "Abbreviation": "document",
            "Description": "document",
            "Data Type": "NONE",
            "Base": "HEX",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "1",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 221.0,
                "y": 1184.0
            },
            "Type": "Field",
            "next_field": "END"
        }
    },
    "path": "/Users/danielornelas/projects/protocol-dissector-builder/Protocol-Dissector-Builder/SAMPLE/MongoDB.pdbproj"
}

test_json4 = {
    "name": "mongodb",
    "created": "12/02/2019 16:39:56",
    "author": "Daniel O",
    "dissector": {
        "START": "CodeBlock0",
        "CodeBlock0": {
            "Code": "length = buffer:len()",
            "Position": {
                "x": 300.0,
                "y": 228.0
            },
            "Type": "CodeBlock",
            "next_field": "Decision0"
        },
        "Decision0": {
            "Condition": {
                "operand1": "length",
                "operator1": "==",
                "operand2": "0"
            },
            "Position": {
                "x": 301.0,
                "y": 301.0
            },
            "true": "CodeBlock1",
            "false": "message_length",
            "Type": "Decision"
        },
        "CodeBlock1": {
            "Code": "return",
            "Position": {
                "x": 623.0,
                "y": 373.0
            },
            "Type": "CodeBlock",
            "next_field": "END"
        },
        "message_length": {
            "Name": "message_length",
            "Abbreviation": "message_length",
            "Description": "messageLength",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 259.0,
                "y": 373.0
            },
            "Type": "Field",
            "next_field": "request_id"
        },
        "request_id": {
            "Name": "request_id",
            "Abbreviation": "request_id",
            "Description": "RequestID",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 260.0,
                "y": 438.0
            },
            "Type": "Field",
            "next_field": "response_to"
        },
        "response_to": {
            "Name": "response_to",
            "Abbreviation": "response_to",
            "Description": "responseTo",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 260.0,
                "y": 503.0
            },
            "Type": "Field",
            "next_field": "CodeBlock3"
        },
        "CodeBlock3": {
            "Code": " local opcode_number = buffer(12,4):le_uint()\n    local opcode_name = get_opcode_name(opcode_number)",
            "Position": {
                "x": 261.0,
                "y": 566.0
            },
            "Type": "CodeBlock",
            "next_field": "opcode"
        },
        "opcode": {
            "Name": "opcode",
            "Abbreviation": "opcode",
            "Description": "opCode",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 261.0,
                "y": 622.0
            },
            "Type": "Field",
            "next_field": "Decision1"
        },
        "Decision1": {
            "Condition": {
                "operand1": "opcode_name",
                "operator1": "==",
                "operand2": "\"OP_QUERY\""
            },
            "Position": {
                "x": 261.0,
                "y": 702.0
            },
            "true": "CodeBlock4",
            "false": "Decision3",
            "Type": "Decision"
        },
        "CodeBlock4": {
            "Code": "local flags_number = buffer(16,4):le_uint()\n        local flags_description = get_flag_description(flags_number)",
            "Position": {
                "x": 632.0,
                "y": 756.0
            },
            "Type": "CodeBlock",
            "next_field": "flags"
        },
        "flags": {
            "Name": "flags",
            "Abbreviation": "flags",
            "Description": "flags",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 663.0,
                "y": 855.125
            },
            "Type": "Field",
            "next_field": "CodeBlock5"
        },
        "CodeBlock5": {
            "Code": "local string_length",
            "Position": {
                "x": 673.0,
                "y": 953.3125
            },
            "Type": "CodeBlock",
            "next_field": "ForLoop0"
        },
        "ForLoop0": {
            "Expressions": {
                "exp1": "i=20",
                "exp2": "length-1",
                "exp3": "1"
            },
            "Position": {
                "x": 603.75,
                "y": 1032.0
            },
            "true": "Decision2",
            "false": "full_coll_name",
            "Type": "for"
        },
        "Decision2": {
            "Condition": {
                "operand1": "buffer(i,1):le_uint()",
                "operator1": "==",
                "operand2": "0"
            },
            "Position": {
                "x": 963.0,
                "y": 1056.4375
            },
            "true": "CodeBlock6",
            "false": "End_ForLoop0",
            "Type": "Decision"
        },
        "CodeBlock6": {
            "Code": "  string_length = i - 20\n                break",
            "Position": {
                "x": 1115.0,
                "y": 1147.0
            },
            "Type": "CodeBlock",
            "next_field": "END"
        },
        "End_ForLoop0": {
            "Position": {
                "x": 797.4375,
                "y": 1145.5625
            },
            "Type": "End Loop",
            "next_field": "ForLoop0"
        },
        "full_coll_name": {
            "Name": "full_coll_name",
            "Abbreviation": "full_coll_name",
            "Description": "fullCollectionName",
            "Data Type": "STRING",
            "Base": "ASCII",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "message_length",
                "combobox": "Field"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 532.0,
                "y": 1103.0
            },
            "Type": "Field",
            "next_field": "number_to_skip"
        },
        "number_to_skip": {
            "Name": "number_to_skip",
            "Abbreviation": "number_to_skip",
            "Description": "numberToSkip",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 533.0,
                "y": 1192.0
            },
            "Type": "Field",
            "next_field": "number_to_return"
        },
        "number_to_return": {
            "Name": "number_to_return",
            "Abbreviation": "number_to_return",
            "Description": "numberToReturn",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 478.0,
                "y": 1244.0
            },
            "Type": "Field",
            "next_field": "query"
        },
        "query": {
            "Name": "query",
            "Abbreviation": "query",
            "Description": "query",
            "Data Type": "NONE",
            "Base": "HEX",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "1",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 782.0,
                "y": 1249.0
            },
            "Type": "Field",
            "next_field": "END"
        },
        "Decision3": {
            "Condition": {
                "operand1": "opcode_name",
                "operator1": "==",
                "operand2": "\"OP_REPLY\""
            },
            "Position": {
                "x": 196.0,
                "y": 794.0
            },
            "true": "response_flags",
            "false": "END",
            "Type": "Decision"
        },
        "response_flags": {
            "Name": "response_flags",
            "Abbreviation": "response_flags",
            "Description": "responseFlags",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 297.0,
                "y": 931.0
            },
            "Type": "Field",
            "next_field": "cursor_id"
        },
        "cursor_id": {
            "Name": "cursor_id",
            "Abbreviation": "cursor_id",
            "Description": "cursorId",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "8",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 297.0,
                "y": 990.0
            },
            "Type": "Field",
            "next_field": "starting_from"
        },
        "starting_from": {
            "Name": "starting_from",
            "Abbreviation": "starting_from",
            "Description": "startingFrom",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 257.0,
                "y": 1054.0
            },
            "Type": "Field",
            "next_field": "number_returned"
        },
        "number_returned": {
            "Name": "number_returned",
            "Abbreviation": "number_returned",
            "Description": "numberReturned",
            "Data Type": "INT32",
            "Base": "DEC",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "4",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 232.0,
                "y": 1116.0
            },
            "Type": "Field",
            "next_field": "document"
        },
        "document": {
            "Name": "document",
            "Abbreviation": "document",
            "Description": "document",
            "Data Type": "NONE",
            "Base": "HEX",
            "Mask": "",
            "Value Constraint": "",
            "Var Size": {
                "editText": "1",
                "combobox": "BYTES"
            },
            "ID Value": "",
            "Required": "false",
            "LE": "true",
            "Position": {
                "x": 221.0,
                "y": 1184.0
            },
            "Type": "Field",
            "next_field": "END"
        }
    },
    "path": "/Users/danielornelas/projects/protocol-dissector-builder/Protocol-Dissector-Builder/SAMPLE/MongoDB.pdbproj"
}

def test_parse_json_correct_json():
    diss = Dissector_Generator()
    diss.parse_json(test_json)

    assert diss.dissector['name'] == "mongodb"
    assert diss.dissector['description'] == "mongodb Protocol"
    assert diss.dissector['subtree_name'] == "mongodb"
    assert diss.dissector['port_type'] == 'tcp'
    assert diss.dissector['port_number'] == "27017"

def test_parse_json_empty_json():
    with pytest.raises(Exception) as e_info:
        diss = Dissector_Generator()
        diss.parse_json(test_json2)
        

def test_parse_json_missing_json():
    with pytest.raises(Exception) as e_info:
        diss = Dissector_Generator()
        diss.parse_json()

def test_parse_json_improperly_formatted_json():
    with pytest.raises(Exception) as e_info:
        diss = Dissector_Generator()
        diss.parse_json(test_json3)


def test_parse_json_missing_attributes_json():
    with pytest.raises(Exception) as e_info:
        diss = Dissector_Generator()
        diss.parse_json(test_json4)

#def test
    