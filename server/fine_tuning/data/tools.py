tools = [
    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": "Use this tool to save memories like user information to storage",
            "parameters": {
                "properties": {"memory": {"type": "string"}},
                "required": ["memory"],
                "type": "object",
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_documents",
            "description": 'Retrieve shop documents for queries about store services like policies, FAQs, or categories. Use for intent `service`.\n\nCategories:\n- faqs: General queries like "How to cancel an order."\n- policies: Detailed policy inquiries like "What is your refund policy?"\n\nExample:\n- Query: "What are your policies?" → Category: [policies]\n\nUse only when `intent = service`.',
            "parameters": {
                "properties": {
                    "document_request": {
                        "properties": {
                            "query": {"type": "string"},
                            "service_categories": {
                                "items": {"type": "string"},
                                "maxItems": 2,
                                "minItems": 0,
                                "type": "array",
                            },
                        },
                        "required": ["query", "service_categories"],
                        "type": "object",
                    }
                },
                "required": ["document_request"],
                "type": "object",
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sql_db_schema",
            "description": "Get the schema and sample rows for the specified SQL tables.Use after verifying table names.Prerequisite: Call sql_db_list_tables first if tables are unknown.",
            "parameters": {
                "properties": {
                    "table_names": {
                        "description": "A comma-separated list of the table names for which to return the schema. Example input: 'table1, table2, table3'",
                        "type": "string",
                    }
                },
                "required": ["table_names"],
                "type": "object",
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sql_db_list_tables",
            "description": "Get database table names\nInput is an empty string, output is a comma-separated list of tables in the database. Call this only if table names are unknown.\n",
            "parameters": {
                "properties": {
                    "tool_input": {
                        "default": "",
                        "description": "An empty string",
                        "type": "string",
                    }
                },
                "type": "object",
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_and_execute_query_tool",
            "description": "Validate and execute SQL queries.\n\nRequirements:\n- Prior calls to sql_db_list_tables and sql_db_schema.\n- Ensure SQL syntax correctness.\n\nExample query: \"SELECT * FROM Product WHERE name LIKE '%cotton%';\"\n\nReturns: Query result or error for retry.",
            "parameters": {
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
                "type": "object",
            },
        },
    },
]
