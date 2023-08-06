definitions {}
title = "Span configuration schema v1.0"
type = "object"
required = ["version"]

anyOf = [
    {required = ["features"]},
    {required = ["train"]},
    # serving requires a train to reference what to serve.
    {required = ["train", "serve"]},
]

properties "version" { type = "string" }

properties "features" {
    type = "object"
    required = ["image", "script", "feature_definition"]
    properties {
        image {
            type = "string"
        }
        install {
            type = "array"
            items { type = "string" }
        }
        script {
            type = "array"
            items {
                oneOf = [
                    # Deprecated, keeping for backwards compatibility
                    {type = "string"},
                    {
                        type = "object",
                        oneOf = [
                            { required = ["sh"]},
                            { required = ["spark-submit"]}
                        ]
                        properties {
                            sh {
                                type = "array"
                                items { type= "string" }
                            }
                            spark-submit {
                                type = "object"
                                properties {
                                    script {
                                        type = "string"
                                    }
                                    conf {
                                        type = "object"
                                        additionalProperties {
                                            type = "string"
                                        }
                                    }
                                    settings {
                                        type = "object"
                                        additionalProperties {
                                            type = "string"
                                        }
                                    }
                                }
                            }
                        }
                    },
                ]
            }
        }
        parameters {
            type = "object"
            additionalProperties {
                type = "string"
            }
        }
        secrets {
            type = "array"
            items { type = "string" }
        }
        # Deprecated, keeping for backwards compatibility
        # Use script/spark-submit instead
        spark {
            type = "object"
            properties {
                conf {
                    type = "object"
                    additionalProperties {
                        type = "string"
                    }
                }
                settings {
                    type = "object"
                    additionalProperties {
                        type = "string"
                    }
                }
            }
        }

        feature_definition {
            type = "array"
            items {
                type = "object"
                properties {
                    name {
                        type = "string"
                        # ex valid: name, name_with_numb3r
                        # ex invalid: trailing_underscore_, Name_with_capital, name-with-dash
                        pattern = "^[a-z0-9]+(_[a-z0-9]+)*$"
                    }
                    key {
                        type = "string"
                    }
                    description {
                        type = "string"
                    }
                }
                additionalProperties = false
            }
        }
    }
}

properties "train" {
    type = "object"
    required = ["image", "script"]
    properties {
        image {
            type = "string"
        }
        install {
            type = "array"
            items { type = "string" }
        }
        script {
            type = "array"
            items {
                oneOf = [
                    # Deprecated, keeping for backwards compatability
                    {type = "string"},
                    {
                        type = "object",
                        oneOf = [
                            {
                                required = ["sh"]
                                properties {
                                    sh {
                                        type = "array"
                                        items { type= "string" }
                                    }
                                }
                            },
                            {
                                required = ["spark-submit"]
                                properties {
                                    spark-submit {
                                        type = "object"
                                        properties {
                                            script {
                                                type = "string"
                                            }
                                            conf {
                                                type = "object"
                                                additionalProperties {
                                                    type = "string"
                                                }
                                            }
                                            settings {
                                                type = "object"
                                                additionalProperties {
                                                    type = "string"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                    },
                ]
            }
        }
        parameters {
            type = "object"
            additionalProperties {
                type = "string"
            }
        }
        secrets {
            type = "array"
            items { type = "string" }
        }
        # Deprecated, keeping for backwards compatibility
        # Use script/spark-submit instead
        spark {
            type = "object"
            properties {
                conf {
                    type = "object"
                    additionalProperties {
                        type = "string"
                    }
                }
                settings {
                    type = "object"
                    additionalProperties {
                        type = "string"
                    }
                }
            }
        }
    }
}

properties "batch_score" {
    type = "object"
    required = ["image", "script"]
    properties {
        image {
            type = "string"
        }
        install {
            type = "array"
            items { type = "string" }
        }
        script {
            type = "array"
            items {
                oneOf = [
                    # Deprecated, keeping for backwards compatibility
                    {type = "string"},
                    {
                        type = "object",
                        oneOf = [
                            {
                                required = ["sh"]
                                properties {
                                    sh {
                                        type = "array"
                                        items { type= "string" }
                                    }
                                }
                            },
                            {
                                required = ["spark-submit"]
                                properties {
                                    spark-submit {
                                        type = "object"
                                        properties {
                                            script {
                                                type = "string"
                                            }
                                            conf {
                                                type = "object"
                                                additionalProperties {
                                                    type = "string"
                                                }
                                            }
                                            settings {
                                                type = "object"
                                                additionalProperties {
                                                    type = "string"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                    },
                ]
            }
        }
        parameters {
            type = "object"
            additionalProperties {
                type = "string"
            }
        }
        secrets {
            type = "array"
            items { type = "string" }
        }
        # Deprecated, keeping for backwards compatability
        # Use script/spark-submit instead
        spark {
            type = "object"
            properties {
                conf {
                    type = "object"
                    additionalProperties {
                        type = "string"
                    }
                }
                settings {
                    type = "object"
                    additionalProperties {
                        type = "string"
                    }
                }
            }
        }
    }
}

properties "serve" {
    type = "object"
    required = ["image", "script"]
    properties {
        image {
            type = "string"
        }
        install {
            type = "array"
            items { type = "string" }
        }
        script {
            type = "array"
            items {
                oneOf = [
                    {
                        type = "object"
                        required = ["sh"]
                        properties {
                            sh {
                                type = "array"
                                items { type = "string" }
                            }
                        }
                    },
                    # Deprecated, keeping for backwards compatability
                    {type = "string"},
                ]

            }
        }
    }
}
