import java.util.Arrays;
import java.util.List;
import java.util.Map;

public class LanceDBQuickstart {
    private static final String LanceDB_API_KEY = "sk_...";
    private static final String LanceDB_DB_URL = "https://{your-db-uri}.us-east-1.api.lancedb.com/v1/table/";

    public static void main(String[] args) {
        try {
            LanceDBOperations lanceDB = new LanceDBOperations(LanceDB_API_KEY, LanceDB_DB_URL);
            String tableName = "quickstart_rest_api";

            // download dataset
            List<Map<String, Object>> dataset = Utils.downloadDataset(256);
            System.out.println(dataset.get(0));

            // 1. create table with dataset
            lanceDB.createTableWithData(tableName, dataset);

            // list tables to make sure the table was created
            List<String> tables = lanceDB.listTables();
            System.out.println("\nListing tables:");
            for (String table : tables) {
                System.out.println(table);
            }

            // 2. create a vector index
            lanceDB.createVectorIndex(tableName, "Cosine");
            Map<String, Object> stats = lanceDB.getIndexStats(tableName, "vector_idx");
            Utils.printIndexStats(stats);

            // 3. create a full-text search index
            lanceDB.createFTSIndex(tableName, "text");

            // 4. perform vector search
            List<Float> queryVector = Utils.createQueryVector(384);
            String filter = "label > 2";
            List<String> columns = Arrays.asList("text", "label");
            lanceDB.vectorSearch(tableName, queryVector, 5, columns, filter, "vector_result");
            Utils.decodeArrowStream("vector_result");

            // 5. perform full text search
            String query = "red";
            lanceDB.fullTextSearch(tableName, "text", query);
            Utils.decodeArrowStream("fts_query");

        } catch (Exception e) {
            System.err.println("Error occurred: " + e.getMessage());
            e.printStackTrace();
        }
    }
} 