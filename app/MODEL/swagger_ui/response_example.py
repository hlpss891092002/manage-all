table_item_response_example = {
                  500:{
                       "description": "Server Error",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                            "message": "Can't get table name."}
                            }
                        }
                  },
                  403:{
                       "description": "invalidation token ",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                        "message": f"type: invalidation token : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJtYW5hZ2VBbGwiLCJlbXBsb3llZV9pZCI6"}
                            }
                        }
                  },
                  200:{
                        "description": "get input item",
                        "content": {
                            "application/json": {
                            "example": {"data": ["name", "description"]}
                            }
                        }
                    }
             } 

table_CUD_response_example = {
                  500:{
                       "description": "Server Error",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                            "message": "type: 1062 (23000): Duplicate entry 'a' for key 'category.name'"}
                            }
                        }
                  },
                  403:{
                       "description": "invalidation token ",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                        "message": f"type: invalidation token : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJtYW5hZ2VBbGwiLCJlbXBsb3llZV9pZCI6"}
                            }
                        }
                  },
                  200:{
                        "description": "get input item",
                        "content": {
                            "application/json": {
                            "example": {"ok": True}
                            }
                        }
                    }
             }

table_search_response_example = {
                  500:{
                       "description": "Server Error",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                            "message": "server error"}
                            }
                        }
                  },
                  403:{
                       "description": "invalidation token ",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                        "message": f"type: invalidation token : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJtYW5hZ2VBbGwiLCJlbXBsb3llZV9pZCI6"}
                            }
                        }
                  },
                  200:{
                        "description": "get input item",
                        "content": {
                            "application/json": {
                            "example": {"PageAmount": 1,
                                        "dataAmount": 1,
                                        "startPage": 0,
                                        "data": [
                                                {
                                                    "name": "Phalaenopsis",
                                                    "description": "Phalaenopsis for test"
                                                }]}
                            }
                        }
                    }
             }


