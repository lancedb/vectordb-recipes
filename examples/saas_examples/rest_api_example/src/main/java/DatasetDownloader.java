import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.http.HttpStatus;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.impl.client.DefaultHttpRequestRetryHandler;
import org.apache.http.impl.conn.PoolingHttpClientConnectionManager;
import org.apache.http.util.EntityUtils;
import java.net.URI;
import java.util.*;

public class DatasetDownloader {
    private static final String DATASET_URL = "https://datasets-server.huggingface.co/rows?dataset=sunhaozhepy/ag_news_sbert_keywords_embeddings&config=default&split=test";
    private static final int BATCH_SIZE = 50;
    private static final int MAX_RETRIES = 3;
    private static final ObjectMapper mapper = new ObjectMapper();
    
    private static CloseableHttpClient createHttpClient() {
        PoolingHttpClientConnectionManager cm = new PoolingHttpClientConnectionManager();
        cm.setMaxTotal(5);
        cm.setDefaultMaxPerRoute(5);
        
        return HttpClients.custom()
                .setConnectionManager(cm)
                .setRetryHandler(new DefaultHttpRequestRetryHandler(MAX_RETRIES, true))
                .build();
    }

    public static List<Map<String, Object>> downloadDataset(String hfApiKey, int maxRows) throws Exception {
        List<Map<String, Object>> allRecords = new ArrayList<>();
        int offset = 0;
        boolean hasMore = true;

        try (CloseableHttpClient httpClient = createHttpClient()) {
            while (hasMore && allRecords.size() < maxRows) {
                // Calculate optimal batch size
                int remainingRows = maxRows - allRecords.size();
                int currentBatchSize = Math.min(BATCH_SIZE, remainingRows);
                
                URI uri = new URIBuilder(DATASET_URL)
                    .addParameter("offset", String.valueOf(offset))
                    .addParameter("limit", String.valueOf(currentBatchSize))
                    .build();
                
                HttpGet httpGet = new HttpGet(uri);
                if (hfApiKey != null && !hfApiKey.isEmpty()) {
                    httpGet.setHeader("Authorization", "Bearer " + hfApiKey);
                }

                // Add retry logic
                boolean success = false;
                int retries = 0;
                Exception lastException = null;
                
                while (!success && retries < MAX_RETRIES) {
                    try {
                        String responseBody = httpClient.execute(httpGet, response -> {
                            int statusCode = response.getStatusLine().getStatusCode();
                            if (statusCode != HttpStatus.SC_OK) {
                                throw new RuntimeException("Failed to download dataset batch: " + statusCode);
                            }
                            return EntityUtils.toString(response.getEntity());
                        });
                        
                        JsonNode root = mapper.readTree(responseBody);
                        JsonNode rowsNode = root.get("rows");
                        
                        if (rowsNode == null || rowsNode.size() == 0) {
                            hasMore = false;
                            break;
                        }

                        for (JsonNode row : rowsNode) {
                            if (allRecords.size() >= maxRows) {
                                hasMore = false;
                                break;
                            }
                            
                            Map<String, Object> record = new HashMap<>();
                            JsonNode rowData = row.get("row");
                            record.put("text", rowData.get("text").asText());
                            record.put("label", rowData.get("label").asInt());
                            
                            // Process embedding with proper type safety
                            JsonNode embeddingNode = rowData.get("embedding");
                            if (embeddingNode != null && embeddingNode.isArray()) {
                                List<Float> embedding = new ArrayList<>(384);
                                for (JsonNode value : embeddingNode) {
                                    embedding.add(value.floatValue());
                                }
                                record.put("embedding", embedding);
                            } else {
                                record.put("embedding", Collections.emptyList());
                            }
                            
                            allRecords.add(record);
                        }

                        // Check if we've reached the end of available data
                        JsonNode totalNode = root.get("total");
                        if (totalNode != null && offset + rowsNode.size() >= totalNode.asInt()) {
                            hasMore = false;
                        }

                        System.out.printf("Downloaded batch: offset=%d, records=%d, total so far=%d/%d%n", 
                                        offset, rowsNode.size(), allRecords.size(), maxRows);
                        
                        success = true;
                    } catch (Exception e) {
                        lastException = e;
                        retries++;
                        if (retries < MAX_RETRIES) {
                            System.err.printf("Error downloading batch (attempt %d/%d): %s. Retrying...%n", 
                                            retries, MAX_RETRIES, e.getMessage());
                            // Exponential backoff
                            Thread.sleep(1000 * retries);
                        }
                    }
                }
                
                if (!success) {
                    throw new RuntimeException("Failed to download batch after " + MAX_RETRIES + " attempts", lastException);
                }
                
                offset += currentBatchSize;
                
                // Small delay between requests
                Thread.sleep(100);
            }
        }

        return allRecords;
    }
} 