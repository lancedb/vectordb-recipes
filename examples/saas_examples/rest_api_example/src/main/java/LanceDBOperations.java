import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import org.apache.http.HttpStatus;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.util.EntityUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.arrow.memory.BufferAllocator;
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.VectorSchemaRoot;
import org.apache.arrow.vector.Float4Vector;
import org.apache.arrow.vector.VarCharVector;
import org.apache.arrow.vector.IntVector;
import org.apache.arrow.vector.ipc.ArrowStreamWriter;
import org.apache.arrow.vector.types.pojo.Schema;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
import java.util.Collections;
import org.apache.arrow.vector.complex.FixedSizeListVector;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import java.io.FileOutputStream;
import org.apache.http.entity.ByteArrayEntity;

public class LanceDBOperations {
    private static final ObjectMapper mapper = new ObjectMapper();
    private static final String JSON_CONTENT_TYPE = "application/json";
    
    private final String apiKey;
    private final String baseUrl;
    private final int embeddingDim;

    public LanceDBOperations(String apiKey, String baseUrl) {
        this(apiKey, baseUrl, 384); // Default embedding dimension
    }

    public LanceDBOperations(String apiKey, String baseUrl, int embeddingDim) {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
        this.embeddingDim = embeddingDim;
    }

    public List<String> listTables() throws IOException {
        final List<String> allTables = new ArrayList<>();
        String nextPageToken = null;
        
        try (final CloseableHttpClient httpClient = HttpClients.createDefault()) {
            do {
                // Build URI with proper parameter encoding
                final URI uri = new URIBuilder(baseUrl)
                    .addParameter("page_token", nextPageToken)
                    .build();
    
                final HttpGet request = new HttpGet(uri);
                request.setHeader("x-api-key", apiKey);
                request.setHeader("Accept", JSON_CONTENT_TYPE);
    
                final String jsonResponse = httpClient.execute(request, response -> {
                    final int statusCode = response.getStatusLine().getStatusCode();
                    if (statusCode != HttpStatus.SC_OK) {
                        throw new IOException("HTTP error " + statusCode + ": " + 
                            EntityUtils.toString(response.getEntity()));
                    }
                    return EntityUtils.toString(response.getEntity());
                });
    
                final JsonNode root = mapper.readTree(jsonResponse);
                final JsonNode tablesNode = root.path("tables");
                
                if (!tablesNode.isArray()) {
                    throw new IllegalStateException("Invalid response format - 'tables' is not an array");
                }
    
                tablesNode.forEach(tableNode -> {
                    if (tableNode.isTextual()) {
                        allTables.add(tableNode.asText());
                    }
                });
    
                nextPageToken = root.path("page_token").asText(null);
            } while (StringUtils.isNotBlank(nextPageToken));
        } catch (URISyntaxException e) {
            throw new IllegalArgumentException("Invalid base URL: " + baseUrl, e);
        }
    
        return allTables;
    }

    public void createTableWithData(String tableName, List<Map<String, Object>> records) throws Exception {
        final int CHUNK_SIZE = 100;
        int totalRecords = records.size();
        int processedRecords = 0;

        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            while (processedRecords < totalRecords) {
                final boolean isFirstChunk = (processedRecords == 0);
                int remainingRecords = totalRecords - processedRecords;
                int currentChunkSize = Math.min(CHUNK_SIZE, remainingRecords);
                List<Map<String, Object>> chunk = records.subList(processedRecords, processedRecords + currentChunkSize);
                
                try (BufferAllocator allocator = new RootAllocator()) {
                    Schema schema = Utils.createArrowSchema(embeddingDim);

                    try (VectorSchemaRoot root = VectorSchemaRoot.create(schema, allocator)) {
                        root.setRowCount(currentChunkSize);
                        
                        FixedSizeListVector vectorVector = (FixedSizeListVector) root.getVector("vector");
                        VarCharVector textVector = (VarCharVector) root.getVector("text");
                        IntVector labelVector = (IntVector) root.getVector("label");
                        
                        vectorVector.allocateNew();
                        Float4Vector values = (Float4Vector) vectorVector.getDataVector();
                        values.allocateNew(currentChunkSize * embeddingDim);
                        textVector.allocateNew();
                        labelVector.allocateNew();
                        
                        for (int i = 0; i < currentChunkSize; i++) {
                            Map<String, Object> record = chunk.get(i);
                            
                            textVector.set(i, ((String) record.get("text")).getBytes());
                            labelVector.set(i, (Integer) record.get("label"));
                            
                            vectorVector.setNotNull(i);
                            @SuppressWarnings("unchecked")
                            List<Float> embedding = (List<Float>) record.get("embedding");
                            
                            if (embedding != null && embedding.size() == embeddingDim) {
                                for (int j = 0; j < embedding.size(); j++) {
                                    Float value = embedding.get(j);
                                    values.set(i * embeddingDim + j, value != null ? value : 0.0f);
                                }
                            } else {
                                for (int j = 0; j < embeddingDim; j++) {
                                    values.set(i * embeddingDim + j, 0.0f);
                                }
                            }
                        }
                        
                        values.setValueCount(currentChunkSize * embeddingDim);
                        vectorVector.setValueCount(currentChunkSize);
                        textVector.setValueCount(currentChunkSize);
                        labelVector.setValueCount(currentChunkSize);
                        
                        byte[] arrowBytes;
                        try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
                            try (ArrowStreamWriter writer = new ArrowStreamWriter(root, null, out)) {
                                writer.start();
                                writer.writeBatch();
                                writer.end();
                            }
                            arrowBytes = out.toByteArray();
                        }
                        
                        String endpoint = isFirstChunk ? "/create/" : "/insert/";
                        HttpPost httpPost = Utils.createRequestTemplate(tableName, baseUrl, apiKey, endpoint, false);
                        
                        httpPost.setEntity(new ByteArrayEntity(arrowBytes));

                        final boolean finalIsFirstChunk = isFirstChunk;
                        Utils.executeRequest(httpClient, httpPost, code -> 
                            String.format("Failed to %s table: %d ", 
                                (finalIsFirstChunk ? "create" : "append to"), code)
                        );

                        System.out.printf("Processed chunk: %d-%d of %d %s%n",
                            processedRecords,
                            processedRecords + currentChunkSize,
                            totalRecords,
                            (isFirstChunk ? " (created table)" : " (appended data)"));
                    }
                }
                
                processedRecords += currentChunkSize;
                Thread.sleep(100);
            }
        }
    }

    public void vectorSearch(String tableName, List<Float> queryVector, int k, List<String> columns, String filter, String resultFileName) throws Exception {
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("vector", queryVector);
        requestBody.put("k", k);
        requestBody.put("columns", columns);
        requestBody.put("filter", filter);

        String jsonBody = mapper.writeValueAsString(requestBody);

        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpPost httpPost = Utils.createRequestTemplate(tableName, baseUrl, apiKey, "/query", true);
            httpPost.setEntity(new StringEntity(jsonBody));

            // Use the utility method to execute the request and get the response
            String responseBody = Utils.executeRequestWithResponse(httpClient, httpPost, "perform vector search");

            // Save the raw response to the specified file
            if (responseBody != null) {
                try (FileOutputStream fos = new FileOutputStream(resultFileName)) {
                    fos.write(responseBody.getBytes());
                }
            }
        }
    }

    public void createIndex(String tableName, String indexType, String column, String distanceType) throws Exception {
        // Validate distanceType for different index types
        if (indexType.startsWith("IVF")) {
            // Vector indices require a valid distance type
            if (distanceType == null || distanceType.isEmpty()) {
                throw new IllegalArgumentException("Distance type is required for vector indices");
            }
            // Validate that distanceType is one of the supported types
            if (!Arrays.asList("L2", "Cosine", "Dot", "Hamming").contains(distanceType)) {
                throw new IllegalArgumentException("Invalid distance type: " + distanceType + 
                    ". Supported types are: L2, Cosine, Dot, Hamming");
            }
        } else if (indexType.startsWith("FTS") || indexType.startsWith("BTREE") || 
                  indexType.startsWith("BITMAP") || indexType.startsWith("LABEL_LIST")) {
            // These index types don't use distance type, but we'll use the provided one anyway
            System.out.println("Note: Distance type is not used for " + indexType + " indices");
        }

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("index_type", indexType);
        requestBody.put("column", column);
        requestBody.put("distance_type", distanceType);

        String jsonBody = mapper.writeValueAsString(requestBody);

        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpPost httpPost = Utils.createRequestTemplate(tableName, baseUrl, apiKey, "/create_index/", true);
            httpPost.setEntity(new StringEntity(jsonBody));

            Utils.executeRequest(httpClient, httpPost, "create index");

            Utils.printIndexCreationMessage(indexType, column, distanceType);
            
            // Pass distanceType to waitForIndexReady for vector indices
            if (indexType.startsWith("IVF")) {
                waitForIndexReady(tableName, column + "_idx", distanceType);
            } else {
                waitForIndexReady(tableName, column + "_idx");
            }
        }
    }

    public void createVectorIndex(String tableName, String distanceType) throws Exception {
        // Validate distance type
        if (distanceType == null || distanceType.isEmpty()) {
            distanceType = "L2"; // Default to L2 if not specified
            System.out.println("No distance type specified, using default: L2");
        }
        createIndex(tableName, "IVF_PQ", "vector", distanceType);
    }

    public void createFTSIndex(String tableName, String column) throws Exception {
        // FTS indices don't use distance type but API requires it
        createIndex(tableName, "FTS", column, "L2");
    }

    public void createScalarIndex(String tableName, String indexType, String column) throws Exception {
        // Scalar indices don't use distance type but API requires it
        createIndex(tableName, indexType, column, "L2");
    }

    public void waitForIndexReady(String tableName, String indexName) throws Exception {
        waitForIndexReady(tableName, indexName, null);
    }

    public void waitForIndexReady(String tableName, String indexName, String expectedDistanceType) throws Exception {
        final int MAX_ATTEMPTS = 30;
        final int POLL_INTERVAL = 2000;
        int attempts = 0;

        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            while (attempts < MAX_ATTEMPTS) {
                HttpPost httpPost = Utils.createRequestTemplate(tableName, baseUrl, apiKey, "/index/list/", true);
                httpPost.setEntity(new StringEntity(""));

                String responseBody = Utils.executeRequestWithResponse(httpClient, httpPost, "list indices");
                
                JsonNode root = mapper.readTree(responseBody);
                JsonNode indexes = root.get("indexes");

                if (indexes != null && indexes.isArray()) {
                    boolean indexFound = false;
                    for (JsonNode index : indexes) {
                        JsonNode indexNameNode = index.get("index_name");
                        if (indexNameNode == null) {
                            System.out.println("Warning: Found index without name");
                            continue;
                        }

                        String currentIndexName = indexNameNode.asText();
                        if (currentIndexName.equals(indexName)) {
                            indexFound = true;
                            
                            // Check distance type if expectedDistanceType is provided
                            if (expectedDistanceType != null) {
                                JsonNode distanceTypeNode = index.get("distance_type");
                                if (distanceTypeNode != null) {
                                    String currentDistanceType = distanceTypeNode.asText();
                                    if (!expectedDistanceType.equalsIgnoreCase(currentDistanceType)) {
                                        System.out.printf("Warning: Index '%s' has distance type '%s', expected '%s'%n", 
                                            indexName, currentDistanceType, expectedDistanceType);
                                    }
                                }
                            }
                            
                            JsonNode statusNode = index.get("status");
                            if (statusNode == null) {
                                System.out.println("Warning: Index '" + indexName + "' has no status field");
                                continue;
                            }

                            String status = statusNode.asText();
                            System.out.printf("Index '%s' status: %s%n", indexName, status);

                            switch (status) {
                                case "done":
                                    System.out.println("Index is ready!");
                                    return;
                                case "failed":
                                    throw new RuntimeException("Index creation failed");
                                case "pending":
                                case "indexing":
                                    break;
                                default:
                                    System.out.println("Unknown index status: " + status);
                                    break;
                            }
                        }
                    }
                    
                    if (!indexFound) {
                        System.out.printf("Index '%s' not found in response, waiting...%n", indexName);
                    }
                } else {
                    System.out.println("No indexes found in response, waiting...");
                }

                attempts++;
                if (attempts < MAX_ATTEMPTS) {
                    Thread.sleep(POLL_INTERVAL);
                    System.out.printf("Attempt %d/%d...%n", attempts + 1, MAX_ATTEMPTS);
                }
            }

            throw new RuntimeException("Timeout waiting for index '" + indexName + "' to be ready after " + 
                                     (MAX_ATTEMPTS * POLL_INTERVAL / 1000) + " seconds");
        }
    }

    public Map<String, Object> getIndexStats(String tableName, String indexName) throws Exception {
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpPost httpPost = Utils.createRequestTemplate(tableName, baseUrl, apiKey, "/index/" + indexName + "/stats/", true);
            httpPost.setEntity(new StringEntity("{}"));

            String responseBody = Utils.executeRequestWithResponse(httpClient, httpPost, "get index stats");

            JsonNode stats = mapper.readTree(responseBody);
            
            Map<String, Object> indexStats = new HashMap<>();
            indexStats.put("indexType", stats.get("index_type").asText());
            indexStats.put("distanceType", stats.get("distance_type").asText());
            indexStats.put("indexedRows", stats.get("num_indexed_rows").asLong());
            indexStats.put("unindexedRows", stats.get("num_unindexed_rows").asLong());
            
            long totalRows = stats.get("num_indexed_rows").asLong() + stats.get("num_unindexed_rows").asLong();
            double progress = totalRows > 0 ? (stats.get("num_indexed_rows").asDouble() / totalRows) * 100 : 0;
            indexStats.put("indexingProgress", progress);
            
            return indexStats;
        }
    }

    public void fullTextSearch(String tableName, String column, String query) throws Exception {
        fullTextSearch(tableName, column, query, 3);
    }

    public void fullTextSearch(String tableName, String column, String query, int k) throws Exception {
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            // Use utility method to create request template
            HttpPost httpPost = Utils.createRequestTemplate(tableName, baseUrl, apiKey, "/query", true);
            
            // Build the request body
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("vector", Collections.emptyList()); // Empty vector array for FTS query
            
            // Build the full_text_query object
            Map<String, Object> fullTextQuery = new HashMap<>();
            fullTextQuery.put("columns", Collections.singletonList(column));
            fullTextQuery.put("query", query);
            requestBody.put("full_text_query", fullTextQuery);
            
            // Set k value for number of results
            requestBody.put("k", k);
            
            // Convert to JSON
            String jsonBody = mapper.writeValueAsString(requestBody);
            httpPost.setEntity(new StringEntity(jsonBody));
            
            // Execute request and get binary response
            byte[] responseBytes = Utils.executeRequestWithBinaryResponse(httpClient, httpPost, "perform full text search");
            
            // Save response to file
            if (responseBytes != null) {
                try (FileOutputStream fos = new FileOutputStream("fts_query")) {
                    fos.write(responseBytes);
                    System.out.println("Successfully wrote response to file 'fts_query'");
                }
            }
        }
    }
} 
