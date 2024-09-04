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

auth_get_response_example = {
                  500:{
                       "description": "Server Error",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                            "message": "server error."}
                            }
                        }
                  },
                  403:{
                       "description": "invalidation token ",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                        "message": f"type: invalidation token : eyJhbGciOiJ"}
                            }
                        }
                  },
                  200:{
                        "description": "get input item",
                        "content": {
                          "application/json": {
                            "example":{
                               "iss": "manageAll",
                                    "employee_id": "2024080000",
                                    "sub": "a",
                                    "job_position": "manager",
                                    "exp": 1725553867
                                } 
                              }  
                            }
                    }
             } 

auth_put_response_example = {
                  500:{
                       "description": "Server Error",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                            "message": "server error."}
                            }
                        }
                  },
                  400:{
                       "description": "invalidation token ",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                        "message": "Account or password is incorrect"}
                            }
                        }
                  },
                  200:{
                        "description": "get input item",
                        "content": {
                          "application/json": {
                            "example":{
                                "token": "'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJtYCtdotLZ6W7Ig"
                                } 
                              } 
                                    
                                  }
                    }
             } 

staff_tables_response_example = {
                  500:{
                       "description": "Server Error",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                            "message": "server error."}
                            }
                        }
                  },
                  403:{
                       "description": "invalidation token ",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                        "message": f"type: invalidation token : eyJhbGciOiJ"}
                            }
                        }
                  },
                  200:{
                        "description": "get input item",
                        "content": {
                          "application/json": {
                            "example":[
                                      "category",
                                      "client",
                                      "client_order",
                                      "media",
                                      "produce_record",
                                      "staff",
                                      "stage",
                                      "variety"
                                  ]
                              }  
                            } 
                    }
             } 

latest_response_example = {
                  500:{
                       "description": "Server Error",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                            "message": "server error."}
                            }
                        }
                  },
                  403:{
                       "description": "invalidation token ",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                        "message": f"type: invalidation token : eyJhbGciOiJ"}
                            }
                        }
                  },
                  200:{
                        "description": "get input item",
                        "content": {
                          "application/json": {
                            "example":{
                      "categoryYesterdayProduce": {},
                      "sevenDaysOuts": {
                          "data": [],
                          "image": "data:image/png;base64, image base64 encode"
                      },
                      "readyShippingStock": {
                          "data": [
                              {
                                  "category": "Philodendron",
                                  "count": 44543
                              },
                              {
                                  "category": "Anthurium",
                                  "count": 43452
                              }
                          ],
                          "image": "data:image/png;base64, image base64 encode"
                      },
                      "categoryStock": {
                          "data": [
                              {
                                  "category": "Platycerium",
                                  "count": 71527
                              },
                              
                          ],
                          "image": "data:image/png;base64, image base64 encode"
                      }
                  }
                              }  
                            } 
                        
                    }
             } 

foreign_list_response_example = {
                  500:{
                       "description": "Server Error",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                            "message": "server error."}
                            }
                        }
                  },
                  403:{
                       "description": "invalidation token ",
                        "content": {
                            "application/json": {
                            "example": {"error": True,
                        "message": f"type: invalidation token : eyJhbGciOiJ"}
                            }
                        }
                  },
                  200:{
                        "description": "get input item",
                        "content": {
                          "application/json": {
                            "example":{
                              "data":["client","variety_code","amount","creation_date","shipping_date"]
                             }
                              }  
                            } 
                        
                    }
             } 