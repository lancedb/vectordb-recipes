import java.io.*;
import java.nio.channels.FileChannel;
import java.util.*;
import org.apache.arrow.memory.RootAllocator;
import org.apache.arrow.vector.Float4Vector;
import org.apache.arrow.vector.IntVector;
import org.apache.arrow.vector.VarCharVector;
import org.apache.arrow.vector.VectorSchemaRoot;
import org.apache.arrow.vector.FieldVector;
import org.apache.arrow.vector.complex.FixedSizeListVector;
import org.apache.arrow.vector.ipc.ArrowFileReader;
import org.apache.arrow.vector.ipc.ArrowStreamReader;
import org.apache.arrow.vector.types.pojo.Field;
import org.apache.arrow.vector.types.pojo.Schema;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.util.EntityUtils;
import org.apache.arrow.vector.types.pojo.ArrowType;
import org.apache.arrow.vector.types.FloatingPointPrecision;
import org.apache.arrow.vector.types.pojo.FieldType;
import org.apache.http.HttpStatus;
import java.util.function.Function;
import org.apache.http.HttpResponse;

public class Utils {
    private static final String JSON_CONTENT_TYPE = "application/json";
    private static final String ARROW_STREAM_CONTENT_TYPE = "application/vnd.apache.arrow.stream";


    public static List<Map<String, Object>> downloadDataset(int maxRows) throws Exception {
        return downloadDataset(0, maxRows);
    }

    public static List<Map<String, Object>> downloadDataset(int offset, int maxRows) throws Exception {
        // Call the DatasetDownloader with null API key (not required for this dataset)
        return DatasetDownloader.downloadDataset(null, maxRows);
    }

    public static Schema createArrowSchema(int embeddingDim) {
        Field vectorElementField = new Field("item", 
            FieldType.nullable(new ArrowType.FloatingPoint(FloatingPointPrecision.SINGLE)), null);
            
        Field vectorField = new Field("vector",
            FieldType.nullable(new ArrowType.FixedSizeList(embeddingDim)),
            Collections.singletonList(vectorElementField));
            
        Field textField = new Field("text",
            FieldType.nullable(new ArrowType.Utf8()), null);
            
        Field labelField = new Field("label",
            FieldType.nullable(new ArrowType.Int(32, true)), null);
            
        return new Schema(Arrays.asList(vectorField, textField, labelField));
    }

    public static void validateAllRecords(List<Map<String, Object>> records, int expectedDim) {
        records.parallelStream().forEach(record -> {
            List<?> embedding = (List<?>) record.get("embedding");
            if (embedding == null || embedding.size() != expectedDim) {
                throw new IllegalArgumentException("Invalid embedding size. Expected " + 
                    expectedDim + " but got " + (embedding == null ? "null" : embedding.size()));
            }
        });
    }
    
    public static HttpPost createRequestTemplate(String tableName, String baseUrl, String apiKey, String endpoint, Boolean isJson) {
        HttpPost post = new HttpPost(baseUrl + tableName + "/" + endpoint + "/");
        post.setHeader("x-api-key", apiKey);
        if (isJson) {
            post.setHeader("Content-Type", JSON_CONTENT_TYPE);
        } else {
            post.setHeader("Content-Type", ARROW_STREAM_CONTENT_TYPE);
        }
        return post;
    }

    public static List<Float> createQueryVector(int vectorDim) throws Exception {
        List<Map<String, Object>> records = downloadDataset(1000, 1);
        Map<String, Object> record = records.get(0);
        Object embObj = record.get("embedding");
        if (!(embObj instanceof List<?>)) {
            throw new IllegalArgumentException("Expected embedding to be a List");
        }
        
        @SuppressWarnings("unchecked") 
        List<Float> embedding = (List<Float>) embObj;
        
        // Create a new fixed-size list
        List<Float> result = new ArrayList<>(vectorDim);
        for (int i = 0; i < vectorDim && i < embedding.size(); i++) {
            result.add(embedding.get(i));
        }
        return result;
    }

    public static void printIndexStats(Map<String, Object> stats) {
        System.out.println("\nIndex Statistics:");
        System.out.println("----------------");
        String indexType = (String) stats.get("indexType");
        System.out.printf("Index Type: %s%n", indexType);
        if (indexType != null && indexType.startsWith("IVF")) {
            System.out.printf("Distance Type: %s%n", stats.get("distanceType"));
        }
        System.out.printf("Indexed Rows: %d%n", stats.get("indexedRows"));
        System.out.printf("Unindexed Rows: %d%n", stats.get("unindexedRows"));
        System.out.printf("Indexing Progress: %.1f%%%n", stats.get("indexingProgress"));
    }

    public static List<Map<String, Object>> decodeArrowStream(byte[] arrowStreamBytes) throws Exception {
        List<Map<String, Object>> records = new ArrayList<>();
        
        try (ByteArrayInputStream in = new ByteArrayInputStream(arrowStreamBytes);
             ArrowStreamReader reader = new ArrowStreamReader(in, new RootAllocator())) {
            
            VectorSchemaRoot root = reader.getVectorSchemaRoot();
            Schema schema = root.getSchema();
            System.out.println("Schema: " + schema);
            
            while (reader.loadNextBatch()) {
                int rowCount = root.getRowCount();
                
                for (int i = 0; i < rowCount; i++) {
                    Map<String, Object> record = new HashMap<>();
                    
                    for (Field field : root.getSchema().getFields()) {
                        String fieldName = field.getName();
                        FieldVector vector = root.getVector(fieldName);
                        
                        if (vector.isNull(i)) {
                            record.put(fieldName, null);
                            continue;
                        }
                        
                        if (vector instanceof FixedSizeListVector) {
                            FixedSizeListVector listVector = (FixedSizeListVector) vector;
                            int listSize = listVector.getListSize();
                            Float4Vector valueVector = (Float4Vector) listVector.getDataVector();
                            
                            List<Float> values = new ArrayList<>(listSize);
                            for (int j = 0; j < listSize; j++) {
                                values.add(valueVector.get(i * listSize + j));
                            }
                            record.put(fieldName, values);
                        } else if (vector instanceof VarCharVector) {
                            VarCharVector varCharVector = (VarCharVector) vector;
                            record.put(fieldName, new String(varCharVector.get(i)));
                        } else if (vector instanceof IntVector) {
                            IntVector intVector = (IntVector) vector;
                            record.put(fieldName, intVector.get(i));
                        } else {
                            record.put(fieldName, vector.getObject(i));
                        }
                    }
                    
                    records.add(record);
                }
            }
        }
        
        return records;
    }

    public static List<Map<String, Object>> decodeArrowStream(String filePath) throws Exception {
        List<Map<String, Object>> records = new ArrayList<>();
        try (
            FileInputStream file = new FileInputStream(filePath);
            FileChannel channel = file.getChannel();
            ArrowFileReader reader = new ArrowFileReader(channel, new RootAllocator(Long.MAX_VALUE))
            ) {
            VectorSchemaRoot root = reader.getVectorSchemaRoot();
            while (reader.loadNextBatch()) {
                // Process the batch
                System.out.println(root.contentToTSVString());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return records;
    }

    // Core method that handles all HTTP request execution cases
    private static <T> T executeRequestCore(CloseableHttpClient httpClient, HttpPost httpPost, 
                                          Function<Integer, String> errorMessageFormatter,
                                          Function<HttpResponse, T> responseHandler) throws IOException {
        return httpClient.execute(httpPost, response -> {
            int code = response.getStatusLine().getStatusCode();
            if (code != HttpStatus.SC_OK) {
                String errorBody = EntityUtils.toString(response.getEntity());
                throw new RuntimeException(errorMessageFormatter.apply(code) + errorBody);
            }
            return responseHandler.apply(response);
        });
    }
    
    // Simple wrapper for void operations with standard error message
    public static void executeRequest(CloseableHttpClient httpClient, HttpPost httpPost, 
                                      String operationDescription) throws IOException {
        executeRequestCore(
            httpClient, 
            httpPost,
            code -> "Failed to " + operationDescription + ": " + code + "\nError: ",
            response -> null
        );
    }
    
    // Wrapper for void operations with custom error message formatter
    public static void executeRequest(CloseableHttpClient httpClient, HttpPost httpPost, 
                                      Function<Integer, String> errorMessageFormatter) throws IOException {
        executeRequestCore(
            httpClient,
            httpPost,
            errorMessageFormatter,
            response -> null
        );
    }
    
    // Wrapper for operations that return response body as String
    public static String executeRequestWithResponse(CloseableHttpClient httpClient, HttpPost httpPost, 
                                                   String operationDescription) throws IOException {
        return executeRequestCore(
            httpClient,
            httpPost,
            code -> "Failed to " + operationDescription + ": " + code + "\nError: ",
            response -> {
                try {
                    return EntityUtils.toString(response.getEntity());
                } catch (IOException e) {
                    throw new RuntimeException("Failed to read response body", e);
                }
            }
        );
    }

    // Wrapper for operations that return raw binary response data
    public static byte[] executeRequestWithBinaryResponse(CloseableHttpClient httpClient, HttpPost httpPost, 
                                                        String operationDescription) throws IOException {
        return executeRequestCore(
            httpClient,
            httpPost,
            code -> "Failed to " + operationDescription + ": " + code + "\nError: ",
            response -> {
                try {
                    return response.getEntity().getContent().readAllBytes();
                } catch (IOException e) {
                    throw new RuntimeException("Failed to read binary response", e);
                }
            }
        );
    }

    public static void printIndexCreationMessage(String indexType, String column, String distanceType) {
        if (indexType.startsWith("IVF")) {
            System.out.println("Vector index creation started with type=" + indexType + 
                             ", column=" + column + ", distance=" + distanceType);
        } else if (indexType.startsWith("FTS")) {
            System.out.println("Full-text Search index creation started for column=" + column);
        } else if (indexType.startsWith("BTREE") || indexType.startsWith("BITMAP") || 
                   indexType.startsWith("LABEL_LIST")) {
            System.out.println("Scalar index creation started with type=" + indexType + 
                             ", column=" + column);
        } else {
            System.out.println("Index creation started with type=" + indexType + 
                             ", column=" + column + ", distance=" + distanceType);
        }
    }
}  