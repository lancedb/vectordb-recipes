# LanceDB Cloud REST API Java Quickstart

This example demonstrates how to use the LanceDB Cloud REST API with Java, including table creation, data insertion, vector search operations, and index creation.

## Prerequisites

- Java 11 or later
- Maven
- LanceDB Cloud account (API key and database URL)

## Setup

1. Clone this repository
2. Update `LanceDBQuickstart.java`:
   - Replace the `LanceDB_API_KEY` value with your actual LanceDB Cloud API key
   - Update `LanceDB_DB_URL` if your database endpoint is different

## Building and Running

1. Install dependencies using Maven:
```bash
mvn clean install
```

2. Run the example:

Option 1: Using Maven exec plugin:
```bash
mvn exec:java
```

Option 2: Using direct Java command (recommended):
```bash
java --add-opens=java.base/java.nio=ALL-UNNAMED -cp target/classes:$(mvn dependency:build-classpath -Dmdep.outputFile=/dev/stdout -q) LanceDBQuickstart
```

This command:
- Opens up JVM module restrictions required by Arrow
- Builds the classpath dynamically from Maven dependencies
- Runs the LanceDBQuickstart class directly

## Features Demonstrated

This example demonstrates the following operations with LanceDB:

1. **Table Creation**: Creates a table with dynamic schema based on the dataset
2. **Vector Index Creation**: Creates an IVF_PQ vector index for faster vector searches
3. **Full-Text Search Index**: Creates a full-text search index on the text field
4. **Vector Search**: Performs vector similarity search with customizable parameters
5. **Full-Text Search**: Performs text-based search using the full-text index

## Code Structure

- `LanceDBQuickstart.java`: Main example program
- `LanceDBOperations.java`: Core operations for interacting with LanceDB
- `Utils.java`: Utility methods for data processing and HTTP operations
- `DatasetDownloader.java`: Handles dataset acquisition and formatting